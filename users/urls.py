from django.urls import path
from users.view.wallet import WalletView


app_name = 'users'

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
]