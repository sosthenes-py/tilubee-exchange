from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from users.view.wallet import WalletView
from users.forms import ConvertQuoteForm, FilterForm
from payment_utils.tickers import markets as crypto_markets
from payment_utils.funcs import bcdiv
from transactions.models import Conversion
import datetime as dt
from django.db.models import Q
from transactions.view.user_transactions import UserTransactions
from users.models import Notification
from django.utils import timezone



class ConvertView(WalletView):
    def get(self, request):
        return render(request, 'users/convert.html', {'page': 'convert'})

    def post(self, request):
        super_post = super().post(request)
        if super_post is not None:
            return super_post
        elif self.action == 'convert':
            qf = ConvertQuoteForm(request.POST)
            if qf.is_valid():
                quoted = self.sort(qf)
                from_coin = qf.cleaned_data['from_coin']
                to_coin = qf.cleaned_data['to_coin']
                if getattr(self.user.wallet, from_coin) >= qf.cleaned_data['from_qty']:
                    if qf.cleaned_data['action2'] == 'quote':
                        return self.quote(quoted, from_coin, to_coin)
                    elif qf.cleaned_data['action2'] == 'confirm':
                        return self.confirm(quoted, qf)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid input'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Please check your inputs'
            })
        elif self.action == 'filter':
            return self.filter(request)
    
    def sort(self, qf):
        crypto_markets = crypto_market(self.tickers)
        from_coin = qf.cleaned_data['from_coin']
        to_coin = qf.cleaned_data['to_coin']
        from_price_one_usd = 1 / crypto_markets[from_coin]['price']
        to_price_one_usd = 1 / crypto_markets[to_coin]['price']
        quote_price = to_price_one_usd/from_price_one_usd  # This is price of one from_coin in to_coin
        quote_qty = quote_price * qf.cleaned_data['from_qty']
        return {
            'price': quote_price,
            'qty': quote_qty
        }
    
    def quote(self, quoted, from_coin, to_coin):
        return JsonResponse({
            'status': 'success',
            'quote_price': quoted['price'],
            'quote_qty': quoted['qty'],
            'ref': f'1 {from_coin.upper()} = {bcdiv(quoted["price"]):,} {to_coin.upper()}',
            'fee': '$0',
            'slippage': '0.1%'
        })
    
    def confirm(self, quoted, qf):
        from_coin = qf.cleaned_data['from_coin']
        to_coin = qf.cleaned_data['to_coin']
        from_bal = getattr(self.user.wallet, from_coin) - qf.cleaned_data['from_qty']
        to_bal = getattr(self.user.wallet, to_coin) + quoted['qty']
        setattr(self.user.wallet, from_coin, from_bal)
        setattr(self.user.wallet, to_coin, to_bal)

        Conversion.objects.create(user=self.user, qty_from=qf.cleaned_data['from_qty'], qty_to=quoted['qty'], currency_from=from_coin, currency_to=to_coin, status='completed')


        Notification.objects.create(user=self.user, title='Conversion Successful', body=f"You have successfully converted {bcdiv(qf.cleaned_data['from_qty']):,} {from_coin.upper()} to {bcdiv(quoted['qty']):,} {to_coin.upper()}.")

        self.user.wallet.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Conversion completed',
            'amount': f'{bcdiv(quoted["qty"]):,} {to_coin.upper()}'
        })
    
    def filter(self, request):
        ff = FilterForm(request.POST)
        if ff.is_valid():
            duration = int(ff.cleaned_data['duration'])
            if duration == 0:
                conversions = Conversion.objects.filter(user=self.user)
            else:
                conversions = Conversion.objects.filter(
                    Q(user=self.user) &
                    Q(created_at__gte=timezone.now() - dt.timedelta(days=duration))
                )
            user_transactions = UserTransactions(user=self.user, query=conversions)  # provides a better structure
            conversions = user_transactions.get_conversions()
            return JsonResponse({
                'status': 'success',
                'data': conversions,
            })
        print(ff.errors)
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid input'
        })
                
