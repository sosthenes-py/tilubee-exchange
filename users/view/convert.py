from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from users.view.wallet import WalletView
from users.forms import ConvertQuoteForm
from transactions.view.crypto import markets as crypto_market, bcdiv
from transactions.models import Conversion


class ConvertView(WalletView):
    def get(self, request):
        return render(request, 'users/convert.html')

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
                    else:
                        return self.confirm(quoted, qf)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid input'
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Please check your inputs'
            })
    
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
            'ref': f'1 {from_coin.upper()} = {bcdiv(quoted['price']):,} {to_coin.upper()}',
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

        self.user.wallet.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Conversion completed',
            'amount': f'{bcdiv(quoted["qty"]):,} {to_coin.upper()}'
        })
                
