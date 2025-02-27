import random

from django.db import transaction
from django.views import View
from payment_utils.models import Ticker
from django.http import JsonResponse
from transactions.models import Transaction
from users.forms import WithdrawalForm
from decimal import Decimal
from payment_utils.tickers import markets as crypto_markets, COINS_DICT
from payment_utils.funcs import bcdiv
from users.models import UserBankAccount, Notification


class WithdrawalView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user = None
        self.base_currency = 'usdt'
        self.tickers = Ticker.objects.all()
        self.one_usd_in_base = None


    def post(self, request):
        self.user = request.user
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            if not self.user.transactions.filter(status='pending', transaction_type='withdrawal').exists():
                action = form.cleaned_data.get('action')
                if action == 'retrieve_banks':
                    return self.account()
                return self.initiate_withdrawal(action, form)
            return JsonResponse({
                'status': 'error',
                'message': 'You have a pending withdrawal. Please wait'
            })
        return JsonResponse({
            'success': 'error',
            'message': 'An error occurred, please refresh page and try again',
        })

    def account(self):
            banks = self.user.user_bank_accounts.all().order_by('-created_at').values()
            return JsonResponse({
                'status': 'success',
                'banks': list(banks)
            })

    def initiate_withdrawal(self, action, form):
        if action in ('crypto', 'uid', 'bank'):
            result, d = self.validate_withdrawal(form)
            if result:
                with transaction.atomic():
                    setattr(self.user.assets, d['currency'], d['diff'])  # set new balance for wallet
                    self.user.assets.save()

                    amount_usd = crypto_markets(self.tickers)[d['currency']]['price'] * d['qty']
                    Transaction.objects.create(user=self.user, currency=d['currency'], qty=d['qty'], address=d['address'], transaction_type='withdrawal', medium=action, reference=d['platform'], amount_usd=amount_usd)

                    Notification.objects.create(user=self.user, title='Withdrawal Has Been Created', body=f'You have initiated a {action.upper()} withdrawal of {d["qty"]:,} {d["currency"].upper()}, which is being processed.')

                    return self.prepared_response(action, d)
            return JsonResponse(d)
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred, please refresh page and try again',
        })


    def validate_withdrawal(self, form):
        currency = form.cleaned_data.get('currency')
        qty = form.cleaned_data.get('amount')
        platform = form.cleaned_data.get('platform')
        address = form.cleaned_data.get('wallet')
        bank_id = form.cleaned_data.get('bank_id')
        if currency != '' and qty != '' and qty > 0 and address != '' and platform != '':
            if currency in list(COINS_DICT.keys()):
                bank = UserBankAccount.objects.filter(user=self.user, id=bank_id).first()
                if currency == 'ngn' and bank is not None or currency != 'ngn':
                    if qty >= crypto_markets(self.tickers)[currency]['min']:
                        qty = Decimal(qty)
                        bal = Decimal(getattr(self.user.assets, currency))
                        if bal >= qty:
                            diff = bal - qty
                            return True, {
                                'currency': currency,
                                'qty': float(qty),
                                'diff': float(diff),
                                'platform': platform,
                                'address': address,
                                'bank': bank
                            }
                        print('kk')
                    print(f'pp -{qty}')
                print('oo')
            print('aa')
        return False, {
            'status': 'error',
            'message': 'Withdrawal could not be processed.'
        }

    def prepared_response(self, action, d):
        one_usd_in_curr = crypto_markets(self.tickers)[d['currency']]['price']
        amount_in_usd = bcdiv(one_usd_in_curr * d['qty'])
        if action == 'crypto':
            medium = 'crypto'
        else:
            if action == 'uid':
                medium = f'{d["platform"].upper()} UID'
            else:
                medium = f'Bank Transfer ({d["bank"].number[:4]}***)'
        return JsonResponse({
            'status': 'success',
            'message': 'Withdrawal initiated',
            'amount': f'{d["qty"]:,} {d["currency"].upper()} (${amount_in_usd:,})',
            'medium': medium
        })


