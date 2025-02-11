from django.urls import path

from users.view.convert import ConvertView
from users.view.deposit import DepositView
from users.view.withdrawal import WithdrawalView
from users.view.wallet import WalletView
from users.view.settings import SettingsView


app_name = 'users'

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('convert/', ConvertView.as_view(), name='convert')
]