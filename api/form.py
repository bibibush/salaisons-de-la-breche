from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30)

class RegisterForm(UserCreationForm):

    class Meta:
        model = Users #personal User model
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "adresse",
            "phonenumber",
        )

