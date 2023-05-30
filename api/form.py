from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.EmailInput)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=100, widget=forms.EmailInput)
    phonenumber = forms.CharField(max_length=20,widget=forms.TextInput)
    username = forms.CharField(max_length=50, widget=forms.TextInput)
    adresse = forms.CharField(max_length=50, widget=forms.TextInput)

    class Meta:
        model = Users
        fields = (
            "username",
            "email",
            "adresse",
            "phonenumber",
            "password1",
            "password2",
        )
    