from django.urls import path
import user_auth.views as user_auth_views
from user_auth.view.registration import RegistrationView
from user_auth.view.login import LoginView
from user_auth.view.email_verification import EmailVerificationView
from django.contrib.auth.views import LogoutView


app_name = 'user_auth'

urlpatterns = [
    path('', user_auth_views.boarding, name='board'),
    path('boarding/<int:page>', user_auth_views.boarding, name='boarding'),
    path('boarding-final/', user_auth_views.last_boarding, name='last_boarding'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('accounts/login/', user_auth_views.account_login, name='loginn'),
    path('auth/register', RegistrationView.as_view(), name='register'),
    path('auth/verify-email', EmailVerificationView.as_view(), name='verify_email'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
]