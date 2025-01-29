from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator, RegexValidator, ValidationError
from users.models import AppUser
from django import forms


def validate_password_confirmation(form):
    password = form.cleaned_data.get('password')
    password_confirmation = form.cleaned_data.get('password_confirmation')

    if password != password_confirmation:
        raise ValidationError({"password_confirmation": "The two password fields must match."})



class RegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        max_length=20, min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'password-field'})
    )
    password = forms.CharField(
        max_length=20, min_length=6,
        validators=[
            RegexValidator(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\.-_!\$%\(\)\=\+#]).{6,20}$',
                message="Must contain at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character"
            )
        ],
        widget=forms.PasswordInput(attrs={'class': 'password-field'})
    )
    accept_terms = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'checked': 'checked', 'class': 'checkbox-terms tf-checkbox'}))
    email = forms.EmailField(validators=[EmailValidator], widget=forms.EmailInput(attrs={'placeholder': 'johnsmith@example.com'}))
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirmation', 'accept_terms', 'phone']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'password_confirmation': 'Confirm Password',
            'password': 'Choose A Strong Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Smith'}),
            'phone': forms.TextInput(attrs={'placeholder': '08123456789'}),
        }

    def clean(self):
        validate_password_confirmation(self)
        return super().clean()


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address', required=True)
    password = forms.CharField(label='Account Password', widget=forms.PasswordInput(attrs={'class': 'password-field'}), required=True)


class EmailVerificationForm(forms.Form):
    digit1 = forms.IntegerField(required=True, max_value=9, min_value=0, widget=forms.NumberInput(attrs={
        'id': 'digit-2',
        'data-next': 'digit-3',
        'data-previous': 'digit-1'
    }))
    digit2 = forms.IntegerField(required=True, max_value=9, min_value=0, widget=forms.NumberInput(attrs={
        'id': 'digit-3',
        'data-next': 'digit-4',
        'data-previous': 'digit-2'
    }))
    digit3 = forms.IntegerField(required=True, max_value=9, min_value=0, widget=forms.NumberInput(attrs={
        'id': 'digit-4',
        'data-next': 'digit-5',
        'data-previous': 'digit-3'
    }))
    digit4 = forms.IntegerField(required=True, max_value=9, min_value=0, widget=forms.NumberInput(attrs={
        'id': 'digit-5',
        'data-next': 'digit-6',
        'data-previous': 'digit-4'
    }))