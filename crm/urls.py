from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'crm'

urlpatterns = [
    path('auth/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('transactions/', views.transactions, name='transactions'),
    path('operators/', views.operators, name='operators'),
    path('blacklist/', views.view_blacklist, name='blacklist'),
    path('automations/<str:program>', views.automations),
    path('test/', views.test, name='test')
]