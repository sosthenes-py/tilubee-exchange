import uuid

from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from user_auth.forms import RegistrationForm
from django.http import JsonResponse
from users.models import AppUser, Notification
import random
from string import digits
from users.email_sender import EmailSender
from user_auth.view.login import update_session
from user_auth.models import EmailVerification
from transactions.models import Asset


def generate_uid(user_id):
    length = 9 - len(str(user_id))
    suffix = "".join([random.choice(digits) for _ in range(length)])
    return f'{user_id}{suffix}'


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'user_auth/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: AppUser = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user.uid = generate_uid(user.id)
            user.save()
            login(request, user)
            update_session(request)

            # Send email
            code = ''.join([random.choice(digits) for _ in range(4)])
            EmailVerification.objects.create(code=f'{code}',user=user)
            Asset.objects.create(user=user)

            EmailSender(reason='registration', email=user.email, name=user.first_name, code=code).send_email()

            Notification.objects.create(user=user, title='Welcome To PROJECT_NAME', body='Your account on PROJECT_NAME has been created successfully. Welcome to limitless possibilities with us.')

            return JsonResponse({
                'status': 'success',
                'message': 'We have sent a code to your email address. Continue to confirm your email'
            })
        return JsonResponse({
            'status': 'warning',
            'errors': form.errors
        })



