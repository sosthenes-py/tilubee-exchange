from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('auth/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('loans/', views.loans, name='loans'),
    path('loans/<str:status>/', views.loans_with_status, name='loans_with_status'),
    path('repayments/', views.repayments, name='repayments'),
    path('logout/', views.logout_user, name='logout'),
    path('waiver/', views.waiver, name='waiver'),
    path('operators/', views.operators, name='operators'),
    path('blacklist/', views.view_blacklist, name='blacklist'),
    path('logs/', views.view_logs, name='logs'),
    path('users/filtered/', views.accepted_users, name='accepted_users'),
    path('automations/<str:program>', views.automations),
    path('test/', views.test, name='test')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
