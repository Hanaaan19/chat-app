from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter username',
            'class': 'form-control'
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter email',
            'class': 'form-control'
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password',
            'class': 'form-control'
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'form-control'
        })


class EmailLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Email"

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your email',
            'class': 'form-control'
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter password',
            'class': 'form-control'
        })