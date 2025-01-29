from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


def custom_login_required(function=None):
    """
    This decorator checks if a user is still in session or has duplicate session and also
    checks if the user has verified their email address.
    If not, it redirects to the email verification page
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_session'):
            return redirect('user_auth:login')
        if request.user.session.uid != request.session.get('user_session'):
            url = reverse('user_auth:login')
            query_param = "?flash=duplicate"
            return redirect(f"{url}{query_param}")
        if not request.user.email_verification.is_verified:
            return redirect('user_auth:verify_email')
        return function(request, *args, **kwargs)
    return wrapper
