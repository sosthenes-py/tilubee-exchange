from django.db import models
from users.models import AppUser


class EmailVerification(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='email_verification')
    is_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=10, null=False)
    verified_at = models.DateTimeField(auto_now=True, null=True)

