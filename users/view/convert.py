from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from users.view.wallet import WalletView


class ConvertView(WalletView):
    def get(self, request):
        return render(request, 'users/convert.html')

    def post(self, request):
        super_post = super().post(request)
        if super_post is not None:
            return super_post
        pass

