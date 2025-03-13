import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TiluBee.settings")
django.setup()

import json
import boto3
from botocore.exceptions import ClientError

from web3 import Web3
from tronpy import Tron
from tronpy.keys import PrivateKey as TronPrivateKey
import stellar_sdk

import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import sign_and_submit
from xrpl.models.transactions import Payment
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import Fee


from payment_utils.env import KMS_KEY_ID
from payment_utils.tickers import COINS_DICT

from bitcoinlib.wallets import Wallet as BitcoinWallet
from bitcoinlib.transactions import Transaction as BitcoinTransaction
from bitcoinlib.keys import Key

from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair as SolanaKeypair
from solders.pubkey import Pubkey

from payment_utils.env import ALCHEMY_URL, KMS_KEY_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY
import base64


from users.models import AppUser, UserWallet


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
        self.web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))  # Ethereum & BSC
        self.tron = Tron(network="mainnet")  # TRON
        self.xrp_client = JsonRpcClient("https://s1.ripple.com:51234/")  # XRP

    def create_wallet(self, user: AppUser, coin, network):
        """Creates a wallet for the specified coin and network."""
        if network == "bitcoin":
            key = Key()
            address = key.address()
            private_key = key.wif()

        elif network in ["erc20", "bep20"]:  # Ethereum or BSC wallets (0x address)
            account = self.web3.eth.account.create()
            address = account.address
            private_key = account.key.hex()

        elif network == "trc20":
            private_key_obj = TronPrivateKey.random()
            address = private_key_obj.public_key.to_base58check_address()
            private_key = private_key_obj.hex()

        elif network == "sol":
            keypair = SolanaKeypair.generate()
            address = str(keypair.public_key)
            private_key = keypair.seed.hex()

        elif network == "xlm":
            keypair = stellar_sdk.Keypair.random()
            address = keypair.public_key
            private_key = keypair.secret

        elif network == "xrp":
            wallet = Wallet.create()
            address = wallet.classic_address
            private_key = wallet.seed

        else:
            raise ValueError(f"Unsupported network: {network}")

        save_pvtkey = self.save_private_key(coin, network, address, private_key, user)
        if save_pvtkey["success"]:
            return {
                "status": "success",
                "coin": coin,
                "network": network,
                "address": address,
            }
        return save_pvtkey["message"]

    def save_private_key(self, coin, network, address, private_key, user):
        try:
            encrypted_key = self.kms.encrypt(private_key)
            enc_key = base64.b64encode(encrypted_key).decode("utf-8")
            UserWallet.objects.create(
                user=user,
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

        elif network == "xlm":
            return self.withdraw_xlm(amount, from_address, to_address, private_key)

        elif network == "xrp":
            return self.withdraw_xrp(amount, from_address, to_address, private_key)

        elif network == "sol":
            return self.withdraw_sol(amount, from_address, to_address, private_key)

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
        """Handles TRX withdrawals (native transactions)."""
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

    def withdraw_xlm(self, amount, from_address, to_address, private_key):
        """Handles Stellar (XLM) withdrawals with fee estimation"""
        try:
            server = stellar_sdk.Server("https://horizon.stellar.org")
            keypair = stellar_sdk.Keypair.from_secret(private_key)
            account = server.load_account(from_address)

            # Get estimated fee
            fee_info = self.estimate_xlm_fee(from_address)
            base_fee = fee_info["base_fee"]

            # Build the transaction
            tx = (
                stellar_sdk.TransactionBuilder(
                    source_account=account,
                    network_passphrase=stellar_sdk.Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=server.fetch_base_fee(),
                )
                .add_text_memo("XLM Transfer")
                .append_payment_op(to_address, str(amount), "XLM")
                .build()
            )

            # Sign and submit the transaction
            tx.sign(keypair)
            response = self.server.submit_transaction(tx)

            return {
                "status": "success",
                "tx_hash": response["hash"],
                "fee": response["fee_charged"] / 1e7,  # Convert stroops to XLM
            }
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
                transaction=tx, wallet=wallet, client=self.xrp_client
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


# Usage Example:
# coinroto = CoinRoto()
# wallet = coinroto.create_wallet("usdt", "trc20")
# withdrawal = coinroto.create_withdrawal("usdt", "trc20", 100, wallet["address"], "TXYZ...receiver")
user = AppUser.objects.first()
roto = CoinRoto()
res = roto.create_wallet(user, "btc", "bitcoin")
print(res)
