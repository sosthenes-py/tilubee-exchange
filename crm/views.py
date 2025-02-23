import json
import subprocess

import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm, LoginForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from crm.models import AdminUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import crm.utils as utils
import datetime as dt
from decouple import config
import os
from django.conf import settings
from firebase_admin import auth as firebase_auth


# Create your views here.
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'User login successful'})
            return JsonResponse({'status': 'error', 'message': 'Invalid phone or password'})
        return JsonResponse({'status': 'warning', 'message': form.errors})
    else:
        form = LoginForm()
        return render(request, 'admin_panel/auth/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        header = request.headers.get('Authorization')
        if header:
            token = header.split('Bearer ')[1]
            try:
                user = firebase_auth.verify_id_token(token, clock_skew_seconds=10)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Invalid token'})
            else:
                user, created = AdminUser.objects.get_or_create(uid=user['uid'], email=user['email'])
                return JsonResponse({'status': 'success', 'message': 'Successfully registered'})
    else:
        return render(request, 'admin_panel/auth/register.html')



def dashboard(request):
    if request.user.level in ('admin', 'team leader'):
        return redirect('analysis')
    elif request.user.level != 'super admin':
        return redirect('loans')
    return render(request, 'admin_panel/dashboard.html')


def users(request):
    if request.method == "GET":
        return render(request, 'admin_panel/users.html')
    posted_data = {}
    for key, value in request.POST.items():
        posted_data[key] = value
    response = utils.UserUtils(request, **posted_data)
    response.process()
    return JsonResponse({'status': response.status, 'content': response.content, 'message': response.message})


def loans(request):
    if request.method == "GET":
        return render(request, 'admin_panel/loans.html',
                      {'app_stages': settings.APP_STAGES.keys(), 'APP_STAGES': settings.APP_STAGES}
                      )
    posted_data = {}
    for key, value in request.POST.items():
        posted_data[key] = value
    response = utils.LoanUtils(request, **posted_data)
    response.process()
    return JsonResponse({'status': response.status, 'content': response.content, 'message': response.message})


@login_required
def loans_with_status(request, status):
    if request.method == "GET":
        if status in ('pending', 'approved', 'declined', 'disbursed', 'overdue', 'partpayment', 'repaid'):
            return render(request, 'admin_panel/loan_with_status.html', {"status": status})
        return HttpResponseBadRequest(status=404)


@login_required
def repayments(request):
    if request.method == "GET":
        return render(request, 'admin_panel/repayments.html')
    posted_data = {}
    for key, value in request.POST.items():
        posted_data[key] = value
    response = utils.LoanUtils(request, **posted_data)
    response.process()
    print(response.status)
    return JsonResponse({'status': response.status, 'content': response.content, 'message': response.message})


@login_required
def waiver(request):
    return render(request, 'admin_panel/waiver.html')


@login_required
def view_blacklist(request):
    return render(request, 'admin_panel/blacklist.html')


@login_required
def view_logs(request):
    return render(request, 'admin_panel/logs.html')


@login_required
def accepted_users(request):
    return render(request, 'admin_panel/accepted_user.html')



@login_required
def operators(request):
    if request.method == "GET":
        return render(request, 'admin_panel/operators.html', {'app_stages': settings.APP_STAGES.keys(), 'APP_STAGES': settings.APP_STAGES})
    posted_data = {}
    for key, value in request.POST.items():
        posted_data[key] = value
    response = utils.AdminUtils(request, **posted_data)
    response.process()
    return JsonResponse({'status': response.status, 'content': response.content, 'message': response.message})


@csrf_exempt
def automations(request, program):
    if request.method == "GET":
        return JsonResponse({'status': f'success: {program}'})

@csrf_exempt
def test(request):
    return HttpResponse("Test success3")
