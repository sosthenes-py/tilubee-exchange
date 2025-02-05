import random

from django.views import View
from transactions.models import Ticker
from admin_panel.models import AccountDetails
from django.http import JsonResponse
from transactions.view.crypto import create_user_wallet
from django.db.models import Q
from transactions.models import Transaction
from users.forms import DepositForm


class DepositView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user = None
        self.base_currency = 'usdt'
        self.tickers = Ticker.objects.all()
        self.one_usd_in_base = None


    def post(self, request):
        self.user = request.user
        form = DepositForm(request.POST)
        if form.is_valid():
            if self.user.transactions.filter(status='pending', transaction_type='deposit').count() < 3:
                action = form.cleaned_data.get('action')
                if action == 'retrieve_bank_account':
                    return self.account('bank')
                elif action == 'retrieve_crypto_wallet':
                    return self.crypto_account(form.cleaned_data.get('currency'))
                elif action == 'retrieve_uid':
                    return self.account('uid', platform=form.cleaned_data.get('platform'))
                else:
                    return self.create_deposit(action, form)
            return JsonResponse({
                'status': 'error',
                'message': 'Too many pending deposits'
            })
        return JsonResponse({
            'success': 'error',
            'message': 'An error occurred, please refresh page and try again',
        })

    def account(self, account_type, platform=None):
        """
        Doesn't make so much sense but this method handles both bank account and uid retrievals
        platform is required for uid retrieval : ('binance' or 'bybit')
        """
        if account_type in ('bank', 'uid'):
            account = AccountDetails.objects.filter(Q(account_type=account_type) | Q(account_type=account_type, platform=platform)).first()
            return JsonResponse({
                'status': 'success',
                # for bank account
                'number': account.number,
                'bank': account.bank,
                'name': account.name,
                'narration': f'{self.user.id}{random.randint(100,999)}',
                # and for uid
                'uid': account.uid,
                'platform': platform,
            })
    
    def crypto_account(self, currency):
        wallet = self.user.user_wallets.filter(currency=currency).first()
        if not wallet:
            try:
                wallet = create_user_wallet(self.user, currency)
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'An error occurred'
                })
        return JsonResponse({
            'status': 'success',
            'currency': wallet.currency,
            'currency_name': wallet.currency_name,
            'network': wallet.network,
            'address': wallet.address
        })

    def create_deposit(self, action, form):
        print(form.cleaned_data)
        if action in ('crypto', 'uid', 'bank'):
            currency = form.cleaned_data.get('currency')
            qty = form.cleaned_data.get('qty')
            reference = form.cleaned_data.get('ref') or form.cleaned_data.get('platform')
            address = form.cleaned_data.get('uid') or form.cleaned_data.get('wallet')
            if currency != '' and qty != '' and reference != '' and address != '':
                Transaction.objects.create(user=self.user, currency=currency, qty=qty, reference=reference,
                                           address=address, transaction_type='deposit', medium=action)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Your account will be updated as soon as your deposit is confirmed'
                })
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid action'
        })
