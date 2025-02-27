from django.db.models import Q, QuerySet
import httpx
import ccxt
from payment_utils.models import Ticker


COINS_DICT = {
    "ada": "Cardano",
    "bch": "Bitcoin Cash",
    "bnb": "BNB Coin",
    "btc": "Bitcoin",
    "busd": "Binance USD",
    "dash": "Dash",
    "doge": "Dogecoin",
    "eth": "Ethereum",
    "ftm": "Fantom",
    "link": "Chainlink",
    "ltc": "Litecoin",
    "matic": "Polygon",
    "ngn": "NGN Naira",
    "neo": "NEO",
    "ont": "Ontology",
    "shib": "Shiba Inu",
    "sol": "Solana",
    "trx": "TRON",
    "ton": "TON",
    "usdc": "USD Coin",
    "usdt": "Tether",
    "wbtc": "Wrapped Bitcoin",
    "xlm": "Stellar Lumens",
    "xmr": "Monero",
    "xrp": "Ripple",
    "yfi": "Yearn.Finance",
    "zec": "Zcash"
}


def markets(tickers: QuerySet = None, order_by='', reload=False):
    """
    Returns all available markets in a dictionary, Eg:
    {
        'btc': {
                    'short': 'btc',
                    'long': 'Bitcoin',
                    'price': '0.00',
                    'change': '0.0',
                },
        'eth': {...},
        ...
    }
    """

    tickers = Ticker.objects.all() if tickers is None else tickers
    if order_by != '':
        tickers = tickers.order_by(order_by)

    tickers_dict = {
        ticker.coin_short: {
            'short': ticker.coin_short,
            'long': ticker.coin_long,
            'min': ticker.min,
            'max': ticker.max,
            'network': ticker.network,
            'price': ticker.price,
            'change': ticker.change,
        }
        for ticker in tickers
    }

    if reload:
        # Get prices from binance api
        prices = fetch_tickers_http(list(tickers_dict))

        # Construct the response in required format
        for symbol, details in tickers_dict.copy().items():
            if symbol in prices:
                # Update tickers_dict with data from binance and leave other symbols as default
                tickers_dict[symbol] = {
                    "short": symbol,
                    "long": details['long'],
                    "price": float(prices[symbol]["price"]),
                    "change": float(prices[symbol]["change"]),
                    "network": details['network'],
                    "min": details['min'],
                    "max": details['max']
                }
        # Update Ticker DB
        tickers_to_update = Ticker.objects.filter(coin_short__in=list(tickers_dict))
        for ticker in tickers_to_update:
            ticker.price = tickers_dict[ticker.coin_short]['price']
            ticker.change = tickers_dict[ticker.coin_short]['change']
        Ticker.objects.bulk_update(tickers_to_update, ['price', 'change'])

    return tickers_dict


def update():
    pass


def fetch_tickers_http(symbols: list[str]):
    symbols = [sym.upper()+'USDT' for sym in symbols]
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter the results to include only requested symbols
        prices = {
            item["symbol"].replace("USDT", "").lower(): {
                "price": item["lastPrice"],
                "change": item["priceChangePercent"]
            }
            for item in data if item["symbol"] in symbols
        }
        return prices
    else:
        raise Exception("Error fetching tickers.")

