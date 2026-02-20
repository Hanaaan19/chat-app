from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2']


class EmailLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['username'].widget.attrs['placeholder'] = "Enter your email"