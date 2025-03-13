import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "TiluBee.settings"

import django

django.setup()

import time
import json
import boto3
from botocore.exceptions import ClientError

from web3 import Web3
from eth_account import Account

from tronpy import Tron
from tronpy.keys import PrivateKey as TronPrivateKey

import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import sign_and_submit
from xrpl.models.transactions import Payment
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import Fee


from payment_utils.env import KMS_KEY_ID
from payment_utils.tickers import COINS_DICT, MAIN_TOKENS
from typing import Optional
import requests

from bitcoinlib.wallets import Wallet as BitcoinWallet
from bitcoinlib.transactions import Transaction as BitcoinTransaction
from bitcoinlib.keys import Key

from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair as SolanaKeypair
from solders.pubkey import Pubkey

from tonsdk.utils import to_nano, bytes_to_b64str
from tonsdk.contract.wallet import WalletV4ContractR2
from tonsdk.crypto import mnemonic_new, mnemonic_to_wallet_key
from tonsdk.provider import ToncenterClient
from tonsdk.contract.wallet import WalletVersionEnum, Wallets as TonWallets

from payment_utils.env import (
    ALCHEMY_ETH_URL,
    ALCHEMY_POLYGON_URL,
    ALCHEMY_ACCESS_KEY,
    KMS_KEY_ID,
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    TON_CENTER_API_KEY,
)
import base64


from users.models import AppUser, UserWallet
from crm.models import BaseWallet, Webhook, WebhookAddress


class KMS:
    """
    This class handles encryption and decryption of private keys
    """

    def __init__(self):
        self.kms_client = boto3.client(
            "kms",
            region_name="us-west-2",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
        self.key_id = KMS_KEY_ID

    def encrypt(self, data):
        try:
            response = self.kms_client.encrypt(
                KeyId=self.key_id, Plaintext=data.encode()
            )
            return response["CiphertextBlob"]
        except ClientError as e:
            print(f"Error encrypting data: {e}")
            return None

    def decrypt(self, encrypted_data):
        try:
            response = self.kms_client.decrypt(CiphertextBlob=encrypted_data)
            return response["Plaintext"].decode()
        except ClientError as e:
            print(f"Error decrypting data: {e}")
            return None


class CoinRoto:
    """
    This class is responsible for creating wallets, creating withdrawals and signing transactions.
    Private keys are not returned, provide user param to store and retrieve keys to DB
    """

    def __init__(self):
        self.kms = KMS()
        self.web3 = Web3(Web3.HTTPProvider(ALCHEMY_ETH_URL))
        self.tron = Tron(network="mainnet")
        self.xrp_client = JsonRpcClient("https://s1.ripple.com:51234/")
        self.ton_client = ToncenterClient(
            base_url="https://toncenter.com/api/v2/jsonRPC", api_key=TON_CENTER_API_KEY
        )
        self.polygon_client = Web3(Web3.HTTPProvider(ALCHEMY_POLYGON_URL))

    def create_wallet(
        self, user: Optional[AppUser] = None, token="", network="", admin=False
    ):
        """Creates a wallet for the specified coin and network. Set admin to True if wallet is for admin"""
        if not admin and not user:
            return {"status": "error", "message": f"Must be for either admin or user"}

        if network == "bitcoin":
            key = Key()
            address = key.address()
            private_key = key.wif()

        elif network in ["erc20", "bep20"]:
            account = self.web3.eth.account.create()
            address = account.address
            private_key = account.key.hex()

        elif network == "trc20":
            private_key_obj = TronPrivateKey.random()
            address = private_key_obj.public_key.to_base58check_address()
            private_key = private_key_obj.hex()

        elif network == "solana":
            keypair = SolanaKeypair.generate()
            address = str(keypair.public_key)
            private_key = keypair.seed.hex()

        elif network == "ripple":
            wallet = Wallet.create()
            address = wallet.classic_address
            private_key = wallet.seed

        elif network == "ton":
            wallet_mnemonics = mnemonic_new()
            _mnemonics, _pub_k, _priv_k, wallet = TonWallets.from_mnemonics(
                wallet_mnemonics, WalletVersionEnum.v3r2, 0
            )
            address = wallet.address.to_string(True, True, True)
            print(address)
            private_key = ",".join(wallet_mnemonics)

        elif network == "polygon":
            account = Account.create()
            private_key = account.key.hex()
            address = account.address

        else:
            return {"status": "error", "message": f"Unsupported network: {network}"}

        save_pvtkey = self.save_private_key(
            token, network, address, private_key, user, admin
        )
        if save_pvtkey["success"]:
            return {
                "status": "success",
                "coin": token,
                "network": network,
                "address": address,
            }
        return save_pvtkey["message"]

    def save_private_key(self, coin, network, address, private_key, user, admin):
        try:
            encrypted_key = self.kms.encrypt(private_key)
            enc_key = base64.b64encode(encrypted_key).decode("utf-8")
            if user:
                UserWallet.objects.create(
                    user=user,
                    currency=coin,
                    currency_name=COINS_DICT[coin],
                    address=address,
                    network=network,
                    key=enc_key,
                )
            elif admin:
                BaseWallet.objects.create(
                    currency=coin,
                    currency_name=COINS_DICT[coin],
                    address=address,
                    network=network,
                    key=enc_key,
                )
        except Exception as e:
            return {"success": False, "message": str(e)}
        else:
            return {"success": True}

    def retrieve_private_key(self, address):
        try:
            wallet = UserWallet.objects.get(address=address)
            enc_key = base64.b64decode(wallet.key)
            return self.kms.decrypt(enc_key)
        except UserWallet.DoesNotExist as e:
            print("Address does not exist!")
            return None

    def create_withdrawal(self, coin, network, amount, from_address, to_address):
        private_key = self.retrieve_private_key(from_address)
        if not private_key:
            return {"status": "error", "message": "Private key not found"}

        if coin == "btc":
            return self.withdraw_btc(amount, from_address, to_address, private_key)

        elif coin == "eth":
            return self.withdraw_eth(amount, from_address, to_address, private_key)

        elif coin == "trx":
            return self.withdraw_trx(amount, from_address, to_address, private_key)

        elif network == "trc20":
            return self.withdraw_trc20(amount, from_address, to_address, private_key)

        elif network in ["erc20", "bep20"]:
            return self.withdraw_erc20_bep20(
                network, amount, from_address, to_address, private_key
            )

        elif network == "xrp":
            return self.withdraw_xrp(amount, from_address, to_address, private_key)

        elif network == "sol":
            return self.withdraw_sol(amount, from_address, to_address, private_key)

        elif network == "ton":
            return self.withdraw_ton(amount, from_address, to_address, private_key)

        elif network == "polygon":
            return self.withdraw_polygon(amount, from_address, to_address, private_key)

        else:
            return {
                "status": "error",
                "message": f"Unsupported network/token: {network}",
            }

    def withdraw_btc(self, amount, from_address, to_address, private_key):
        """
        Handles Bitcoin withdrawals.
        """
        try:
            # Create a wallet using the private key
            key = Key(import_key=private_key)
            wallet = BitcoinWallet.create(
                "temp_wallet",
                keys=[key],
                network="bitcoin",
                witness_type="segwit",
                db_uri=None,
            )

            fee = self.estimate_btc_fee(from_address, to_address, amount)[
                "estimated_fee"
            ]

            # Create and sign the transaction
            tx = BitcoinTransaction()
            tx.add_input(from_address)  # Add the sender's address
            tx.add_output(to_address, amount - fee)  # Specify the recipient and amount
            tx.sign(keys=[key])  # Sign the transaction

            # Broadcast the transaction
            tx_hash = wallet.send_transaction(tx)

            return {"status": "success", "tx_hash": tx_hash, "fee": fee}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def estimate_btc_fee(self, from_address, to_address, amount):
        # Estimate the fee for a Bitcoin transaction

        # Create the transaction
        tx = BitcoinTransaction(network="bitcoin")
        tx.add_input(from_address, amount)
        tx.add_output(to_address, amount)

        tx_size = len(tx.serialize())

        fee_rate = 100  # Default to 100 satoshis per byte for the example. You can get this dynamically.

        # Estimate the fee (transaction size in bytes * fee rate)
        fee = tx_size * fee_rate  # This is the fee in satoshis

        return {"estimated_fee": fee, "tx_size": tx_size, "fee_rate": fee_rate}

    def withdraw_eth(self, amount, from_address, to_address, private_key):
        """Handles ETH withdrawals (native transactions, not ERC-20)"""
        try:
            nonce = self.web3.eth.get_transaction_count(from_address)

            txn = {
                "nonce": nonce,
                "to": to_address,
                "value": self.web3.to_wei(amount, "ether"),
                "gas": 21000,  # Standard gas limit for ETH transfers
                "gasPrice": self.web3.eth.gas_price,
                "chainId": self.web3.eth.chain_id,
            }
            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            gas_used = tx_receipt["gasUsed"]
            gas_price = txn["gasPrice"]
            fee = gas_used * gas_price
            return {"status": "success", "tx_hash": tx_hash.hex(), "fee": fee}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_erc20_bep20(
        self, coin, network, amount, from_address, to_address, private_key
    ):
        try:
            contract = self.web3.eth.contract(
                address=self._get_contract_address(coin, network), abi=self._get_abi()
            )
            txn = contract.functions.transfer(
                to_address, int(amount * 1_000_000)
            ).build_transaction(
                {
                    "from": from_address,
                    "nonce": self.web3.eth.get_transaction_count(from_address),
                    "gas": 100000,
                    "gasPrice": self.web3.eth.gas_price,
                }
            )
            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            gas_used = tx_receipt["gasUsed"]
            gas_price = txn["gasPrice"]
            fee = gas_used * gas_price

            return {"status": "success", "tx_hash": tx_hash.hex(), "fee": fee}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_trx(self, amount, from_address, to_address, private_key):
        """Handles TRX withdrawals (native transactions)"""
        try:
            txn = self.tron.trx.transfer(
                from_address, to_address, int(amount * 1_000_000)
            )  # TRX uses 6 decimals
            signed_txn = self.tron.trx.sign(txn, private_key)
            tx_hash = self.tron.trx.broadcast(signed_txn)

            return {"status": "success", "tx_hash": tx_hash["txid"], "fee": 0}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_trc20(self, coin, amount, from_address, to_address, private_key):
        """Handles TRC20 withdrawals."""
        try:
            contract = self.tron.get_contract(
                self._get_contract_address(coin, "trc20")
            )  # TRC20 USDT
            txn = (
                contract.functions.transfer(to_address, int(amount * 1_000_000))
                .with_owner(from_address)
                .fee_limit(10_000_000)
                .build()
                .sign(TronPrivateKey(bytes.fromhex(private_key)))
            )
            tx_hash = txn.broadcast().wait()
            return {"status": "sent", "tx_hash": tx_hash, "fee": 0}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_ton(self, coin, amount, from_address, to_address, private_key):
        """Send TON from this wallet."""
        try:
            wallet_mnemonics = private_key.split(",")
            mnemonics, _pub_k, _priv_k, wallet = TonWallets.from_mnemonics(
                wallet_mnemonics, WalletVersionEnum.v3r2, 0
            )

            wallet_info = self.ton_client.get_wallet_info(from_address)
            seqno = wallet_info.get("seqno", 0)

            query = wallet.create_transfer_message(
                to_addr=to_address,
                amount=to_nano(float(amount), "ton"),
                payload="message",
                seqno=int(seqno),
            )
            boc = bytes_to_b64str(query["message"].to_boc(False))

            tx_response = self.ton_client.send_transaction(boc)

            tx_hash = tx_response.get("transaction", {}).get("id", None)
            fee = tx_response.get("fee", None)

            return {"status": "error", "tx_hash": tx_hash, "fee": fee}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_xrp(self, coin, amount, from_address, to_address, private_key):
        """Handles XRP withdrawals"""
        try:
            wallet = Wallet(private_key)
            tx = Payment(
                account=from_address,
                amount=str(amount),
                destination=to_address,
            )
            signed_tx = sign_and_submit(
                transaction=payment, wallet=wallet, client=self.xrp_client
            )
            response = self.xrp_client.submit(signed_tx)
            fee = self.estimate_xrp_fee()

            return {
                "status": "success",
                "tx_hash": response["result"]["hash"],
                "fee": fee,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def withdraw_polygon(self, amount, from_address, to_address, private_key):
        """Handles PoS withdrawals (native transactions)"""
        try:
            w3 = self.polygon_client
            nonce = w3.eth.get_transaction_count(from_address)
            gas_price = w3.eth.gas_price
            gas_limit = 21000  # Standard for ETH/MATIC transfers

            # Create transaction
            tx = {
                "nonce": nonce,
                "to": to_address,
                "value": w3.to_wei(amount, "ether"),
                "gas": gas_limit,
                "gasPrice": gas_price,
                "chainId": 137,  # Polygon Mainnet
            }

            # Sign transaction
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)

            # Send transaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            # Calculate fee
            fee = gas_limit * gas_price  # Fee in Wei

            return {
                "status": "success",
                "tx_hash": tx_hash.hex(),
                "fee": w3.from_wei(fee, "ether"),  # Convert fee to MATIC
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def estimate_xrp_fee(self):
        """Fetches the current transaction fee for XRP"""
        response = self.xrp_client.request(Fee())  # Fetch latest network fee
        base_fee = (
            float(response.result["drops"]["base_fee"]) / 1_000_000
        )  # Convert drops to XRP
        return {"estimated_fee": base_fee}

    def withdraw_sol(self, amount, from_address, to_address, private_key):
        """Handles Solana (SOL) withdrawals."""
        try:
            # Convert private key from base64 format
            private_key_bytes = base64.b64decode(private_key)
            sender_keypair = SolanaKeypair.from_secret_key(private_key_bytes)

            # Create transaction
            txn = Transaction().add(
                transfer(
                    TransferParams(
                        from_pubkey=Pubkey(from_address),
                        to_pubkey=Pubkey(to_address),
                        lamports=int(amount * 1_000_000_000),  # Convert SOL to lamports
                    )
                )
            )

            # Send transaction
            response = self.sol_client.send_transaction(txn, sender_keypair)
            fee = CoinRoto.estimate_sol_fee()
            return {"status": "success", "tx_hash": response["result"], "fee": fee}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def estimate_sol_fee():
        """Fetches the estimated transaction fee on the Solana network"""
        client = Client("https://api.mainnet-beta.solana.com")

        # Get the latest blockhash and fee calculator
        response = client.get_recent_blockhash()

        if "result" in response and "value" in response["result"]:
            fee = response["result"]["value"]["feeCalculator"]["lamportsPerSignature"]
            return {
                "estimated_fee_lamports": fee,
                "estimated_fee_sol": fee / 1_000_000_000,
            }  # Convert to SOL
        else:
            return {"error": "Failed to retrieve fee estimate"}

    def _get_contract_address(self, coin: str, network: str) -> str:
        """Return the contract address for a coin"""
        contract_addresses = {
            "usdt": {
                "erc20": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT ERC20 on Ethereum
                "trc20": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
                "bep20": "0x55d398326f99059ff775485246999027b3197955",
                "ton": "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
            },
            "trx": {
                "erc20": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT ERC20 on Ethereum
                "erc20": "TXwZ2ofG2mHjCVyhjz6f7cW8SC5FvC6yBD",  # USDT TRC20 on Tron
            },
        }

        return contract_addresses.get(coin.lower(), {}).get(network)

    def _get_abi(self, coin, network):
        usdt_abi = [
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ]
        return usdt_abi


class Api:
    def __init__(self, token):
        self.network = self._sort_network(token)["network"]
        self.provider = self._sort_network(token)["provider"]

    def webhook(self):
        if self.provider:
            return self.provider(network=self.network)
        raise ValueError("Provder does not exist")

    def _sort_network(self, token):
        token_networks = {
            "eth": {"network": "ETH_MAINNET", "provider": Alchemy},
            "matic": {"network": "MATICMAINNET", "provider": Alchemy},
            "ton": {"network": "ETH_MAINNET", "provider": None},
            "bnb": {"network": "BNB_MAINNET", "provider": Alchemy},
        }
        return token_networks[token]


class Alchemy:
    def __init__(self, **kwargs):
        self.access_key = ALCHEMY_ACCESS_KEY
        self.network = kwargs.get("network")
        self.webhook_type = "ADDRESS_ACTIVITY"
        self.webhook_url = "https://iqtradepro.ca"

    def add_address(self, address):
        wha = WebhookAddress.objects.filter(network=self.network)
        if wha.exists():
            webhook = wha.first().webhook
            if not wha.filter(address=address).exists():
                # add address
                added, res = self._add_address(address, webhook_id=webhook.webhook_id)
                if added:
                    WebhookAddress.objects.create(
                        address=address, webhook=webhook, network=webhook.network
                    )
                    res["status"] = "success"
                    return res
                res["status"] = "error"
                return res
            return {"status": "success"}
        else:
            created, data = self._create_webhook(address)
            if not created:
                return data
            webhook = Webhook.objects.create(
                webhook_id=data["id"], network=data["network"], url=data["webhook_url"]
            )
            WebhookAddress.objects.create(
                address=address, webhook=webhook, network=data["network"]
            )
            return {"status": "success", "message": "successful"}

    def delete_all_webhooks(self):
        whs = self._get_all_webhooks()
        for wh in whs:
            if self._delete_webhook(wh["id"]):
                print("deleted ..")
                time.sleep(1)

    def _get_all_webhooks(self):
        url = "https://dashboard.alchemy.com/api/team-webhooks"
        response = self._send(url=url, method="get")
        return response.json()["data"]

    def _create_webhook(self, address):
        url = "https://dashboard.alchemy.com/api/create-webhook"
        payload = {
            "network": self.network,
            "webhook_type": self.webhook_type,
            "webhook_url": self.webhook_url,
            "addresses": [address],
        }
        response = self._send(url=url, json=payload, method="post")
        if response.status_code == 200:
            return True, response.json()["data"]
        return False, response.json()

    def _add_address(self, address, webhook_id):
        url = "https://dashboard.alchemy.com/api/update-webhook-addresses"
        payload = {
            "addresses_to_add": [address],
            "addresses_to_remove": [],
            "webhook_id": webhook_id,
        }
        response = self._send(url=url, json=payload, method="patch")
        if response.status_code == 200:
            return True, {"message": "address added"}
        return False, response.json()

    def _get_webhook_addresses(self, webhook_id):
        url = "https://dashboard.alchemy.com/api/webhook-addresses"
        params = {"webhook_id": webhook_id, "limit": 100}
        response = self._send(url=url, method="get", params=params)
        return response.json()

    def _delete_webhook(self, webhook_id):
        url = "https://dashboard.alchemy.com/api/delete-webhook"
        params = {"webhook_id": webhook_id}
        response = self._send(url=url, params=params, method="delete")
        if response.status_code == 200:
            return True
        return False

    def _send(self, **kwargs):
        headers = {
            "accept": "application/json",
            "X-Alchemy-Token": self.access_key,
            "content-type": "application/json",
        }
        return requests.request(**kwargs, headers=headers)


roto = CoinRoto()
user = AppUser.objects.first()

# Generate BaseWallet
## Ensure to uncomment block of code inside save_private_key to save successfully
# for token, network in MAIN_TOKENS.item():
#     try:
#         roto.create_wallet(admin=True, token=token, network=network)
#         print(f'{token} wallet created successfully')
#     except Exception as e:
#         print(str(e))

roto.create_wallet(admin=True, token="ton", network="ton")
