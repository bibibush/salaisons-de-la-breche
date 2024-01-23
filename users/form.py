from django import forms

from users.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["create_dt"]