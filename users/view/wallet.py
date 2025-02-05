from dataclasses import field

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from users.mixins import CustomLoginRequiredMixin
from transactions.view.crypto import markets as crypto_markets, bcdiv
from transactions.models import Ticker, Transaction
from transactions.view.user_transactions import UserTransactions
from users.models import UserBankAccount


class WalletView(CustomLoginRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.user = None
        self.base_currency = 'usdt'
        self.tickers = Ticker.objects.all()
        self.one_usd_in_base = None

    def get(self, request):
        return render(request, 'users/wallet.html')

    def post(self, request):
        base = request.POST.get('base')
        self.base_currency = base if base != 'usd' else 'usdt'
        self.user = request.user
        self.one_usd_in_base = 1 / crypto_markets(self.tickers)[self.base_currency]['price']

        action = request.POST.get('action')
        if action == 'onload':
            return self.onload(request)

    def onload(self, request):
        total_balance = self.total_balance()
        wallets = self.all_balance()
        markets = crypto_markets()
        user_transactions = UserTransactions(request.user, self.one_usd_in_base, self.base_currency)
        history = user_transactions.as_list()
        conversions = user_transactions.get_conversions()
        history = history
        recent_conv = conversions[-5:] if conversions else []
        user_banks = UserBankAccount.objects.filter(user=self.user).order_by('-created_at').values()
        return JsonResponse({
            'status': 'success',
            'total_balance': total_balance,
            'wallets': wallets,
            'markets': markets,
            'recent_conv': recent_conv,
            'history': history,
            'user_banks': list(user_banks)
        })


    def all_balance(self, in_usd=False):
        """
        Returns balance of all wallets in a single dictionary
        """
        wallets = self.user.wallet
        balance = {
            field.name: bcdiv(getattr(wallets, field.name)) if not in_usd else (crypto_markets(self.tickers)[field.name]['price'] * getattr(wallets, field.name))
            for field in wallets._meta.fields
            if field.name not in ('id', 'user')
        }
        return balance

    def total_balance(self):
        total = 0
        for coin, balance in self.all_balance(in_usd=True).items():
            total += bcdiv(balance, self.one_usd_in_base)
        return total




