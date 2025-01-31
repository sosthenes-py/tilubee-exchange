from django.views import View
from django.db.models import Q, QuerySet
from transactions.models import Ticker
from users.models import UserWallet


coins_dict = {
    "ada": "Cardano",
    "algo": "Algorand",
    "ar": "Arweave",
    "atom": "Cosmos",
    "avax": "Avalanche",
    "axs": "Axie Infinity",
    "bat": "Basic Attention Token",
    "bch": "Bitcoin Cash",
    "bnb": "BNB Coin",
    "bond": "BarnBridge",
    "btc": "Bitcoin",
    "busd": "Binance USD",
    "cvx": "Convex Finance",
    "dash": "Dash",
    "dcr": "Decred",
    "doge": "Dogecoin",
    "dot": "Polkadot",
    "edu": "EduCoin",
    "eos": "EOS.IO",
    "etc": "Ethereum Classic",
    "eth": "Ethereum",
    "ftm": "Fantom",
    "fxs": "Frax Share",
    "gala": "Gala",
    "gno": "Gnosis",
    "gtc": "Gitcoin",
    "hive": "Hive",
    "inj": "Injective",
    "kava": "Kava",
    "kda": "Kadena",
    "link": "Chainlink",
    "ltc": "Litecoin",
    "mana": "Decentraland",
    "matic": "Polygon",
    "ngn": "Nigerian Naira",
    "neo": "NEO",
    "nmr": "Numeraire",
    "one": "Harmony",
    "ont": "Ontology",
    "paxg": "PAX Gold",
    "qnt": "Quant",
    "shib": "Shiba Inu",
    "sol": "Solana",
    "trx": "TRON",
    "ton": "TON",
    "uni": "Uniswap",
    "usdc": "USD Coin",
    "usdt": "Tether",
    "wbtc": "Wrapped Bitcoin",
    "xlm": "Stellar Lumens",
    "xmr": "Monero",
    "xrp": "Ripple",
    "yfi": "Yearn.Finance",
    "zec": "Zcash"
}

def markets(tickers: QuerySet = None):
    """
    Returns all available markets in a dictionary, Eg:
    {
        'btc': {
                    'short': 'btc',
                    'long': 'Bitcoin',
                    'price': '0.0',
                    'change': '0.0',
                },
        'eth': {...},
        ...
    }
    """
    tickers = Ticker.objects.all() if tickers is None else tickers
    return {
        ticker.coin_short: {
            'short': ticker.coin_short,
            'long': ticker.coin_long,
            'price': ticker.price,
            'change': ticker.change
        }
        for ticker in tickers
    }

def bcdiv(amount, one_usd_in_base=None):
    """
    Returns a more significant figure for amount
    If one_usd_in_base is applied, returns amount in base currency
    """
    if one_usd_in_base is not None:
        amount = amount * one_usd_in_base

    if amount < 0.001:
        amt = f'{amount:.5f}'
    elif 0.001 <= amount < 1:
        amt = f'{amount:.3f}'
    else:
        amt = f'{amount:.2f}'
    return float(amt)

def create_user_wallet(user, currency):
    if currency not in coins_dict.keys:
        raise ValueError(f'Cannot create this wallet because specified currency {currency} does not exist')
    
    address = ''
    wallet = UserWallet.objects.create(user=user, currency=currency, currency_name=coins_dict[currency], address=address)
    return wallet


