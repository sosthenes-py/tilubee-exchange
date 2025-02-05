from django.urls import path

from users.view.deposit import DepositView
from users.view.withdrawal import WithdrawalView
from users.view.wallet import WalletView


app_name = 'users'

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
]