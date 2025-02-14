from django.views import View
from django.shortcuts import render
from users.mixins import CustomLoginRequiredMixin


class Wallet2View(CustomLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/wallet2.html', {'page': 'wallet'})



