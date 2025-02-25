from payment_utils.tickers import COINS_DICT
from users.models import UserWallet


def create_user_wallet(user, currency):
    if currency not in COINS_DICT.keys():
        raise ValueError(f'Cannot create this wallet because specified currency {currency} does not exist')
    
    address = ''
    network = ''
    wallet = UserWallet.objects.create(user=user, currency=currency, currency_name=COINS_DICT[currency], address=address, network=network)
    return wallet


