from django.views import View
from django.shortcuts import render, redirect
from user_auth.forms import EmailVerificationForm
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from string import digits
from user_auth.models import EmailVerification


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            email_verif = getattr(request.user, 'email_verification', None)
            if email_verif and email_verif.is_verified:
                return redirect('user_auth:last_boarding')
        return super().dispatch(request, *args, **kwargs)


class EmailVerificationView(CustomLoginRequiredMixin, View):
    def get(self, request):
        form = EmailVerificationForm()
        return render(request, 'user_auth/email_verification.html', {'form': form})

    def post(self, request):
        operation = request.POST.get('operation', 'verify')
        if operation == 'verify':
            return self.verify(request)
        elif operation == 'resend':
            return self.resend_code(request)

    def resend_code(self, request):
        code = ''.join([random.choice(digits) for _ in range(4)])
        if hasattr(request.user, 'email_verification'):
            request.user.email_verification.delete()
        EmailVerification.objects.create(code=f'{code}', user=request.user)
        EmailSender(reason='registration', email=request.user.email, name=request.user.first_name, code=code).send_email()
        return JsonResponse({
            'status': 'success',
            'message': 'Code has been resent. Please check your email.',
        })

    def verify(self, request):
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = f"{form.cleaned_data['digit1']}{form.cleaned_data['digit2']}{form.cleaned_data['digit3']}{form.cleaned_data['digit4']}"
            if hasattr(request.user, 'email_verification') and code == request.user.email_verification.code:
                request.user.email_verification.is_verified = True
                request.user.email_verification.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Email verification successful',
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Incorrect code',
            })
        return JsonResponse({
            'status': 'warning',
            'message': 'Please enter the code sent to your email',
        })