from django.views import View
from transactions.models import Ticker
from admin_panel.models import AccountDetails
from django.http import JsonResponse
from transactions.view.crypto import create_user_wallet


class DepositView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user = None
        self.base_currency = 'usdt'
        self.tickers = Ticker.objects.all()
        self.one_usd_in_base = None


    def post(self, request):
        self.user = request.user
        action = request.POST.get('action')
        if action == 'retrieve_bank_account':
            return self.account('bank')
        elif action == 'retrieve_crypto_wallet':
            return self.crypto_account(request.POST.get('currency'))
        elif action == 'retrieve_uid':
            self.account('uid')

    def account(self, account_type):
        if account_type in ('bank', 'uid'):
            account = AccountDetails.objects.filter(account_type=account_type).first()
            return JsonResponse({
                'status': 'success',
                'number': account.number,
                'bank': account.bank,
                'name': account.name,
                # and for uid
                'uid': account.uid
            })
    
    def crypto_account(self, currency):
        wallet = self.user.user_wallets.filter(currency=currency).first()
        if not wallet:
            try:
                wallet = create_user_wallet(self.user, currency)
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'An error occured'
                })
        return JsonResponse({
            'status': 'success',
            'currency': wallet.currency,
            'currency_name': wallet.currency_name,
            'address': wallet.address
        })
