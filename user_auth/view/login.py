import django.db
from django.shortcuts import render, redirect
from django.views import View
from user_auth.forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import uuid
from users.models import Session, AppUser, Notification
from django.contrib.auth.hashers import check_password


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # First IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def update_session(request):
    session_uid = str(uuid.uuid4())
    try:
        Session.objects.create(user=request.user, uid=session_uid, ip_address=get_client_ip(request))
    except django.db.IntegrityError:
        Session.objects.get(user=request.user).delete()
        Session.objects.create(user=request.user, uid=session_uid, ip_address=get_client_ip(request))
    finally:
        request.session['user_session'] = session_uid
    return session_uid


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:wallet')
        flash = request.GET.get('flash', '')
        form = LoginForm()
        return render(request, 'user_auth/login.html', {'form': form, 'flash': flash})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = AppUser.objects.get(email=form.cleaned_data['email'])
            except AppUser.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Account does not exist',
                })
            else:
                if check_password(form.cleaned_data['password'], user.password):
                    login(request, user)
                    update_session(request)

                    Notification.objects.create(user=user, title='Login Attempt', body=f'There was a successful login action on your account from the IP: {get_client_ip(request)}')

                    return JsonResponse({
                        'status': 'success',
                        'message': f'Welcome back, {user.first_name}',
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Account does not exist',
                    })

        return JsonResponse({
            'status': 'warning',
            'errors': form.errors
        })



