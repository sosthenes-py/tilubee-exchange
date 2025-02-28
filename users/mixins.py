from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import logout
from users.models import Notification


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    This mixin checks if a user is still in session or has duplicate session and also
    checks if the user has verified their email address.
    If not, it redirects to the email verification page
    """
    def dispatch(self, request, *args, **kwargs):
        if request.resolver_match.app_name in ('users', 'user_auth'):
            if not request.session.get('user_session'):
                return redirect('user_auth:login')
            if request.user.is_authenticated:
                # if request.user.session.uid != request.session.get('user_session'):
                #     logout(request)
                #     url = reverse('user_auth:login')
                #     query_param = "?flash=duplicate"
                #
                #     Notification.objects.create(user=request.user, title='Duplicate Session Detected', body='The system has detected a duplicate session on your account. For security reasons, previous device has been logged out automatically.')
                #
                #     return redirect(f"{url}{query_param}")
                if not request.user.email_verification.is_verified:
                    return redirect('user_auth:verify_email')
                if request.user.is_blacklisted():
                    logout(request)
                    url = reverse('user_auth:login')
                    query_param = "?flash=blacklist"
                    return redirect(f"{url}{query_param}")
            return super().dispatch(request, *args, **kwargs)
