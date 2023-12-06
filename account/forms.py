from django import forms


class UserRegistrationForms(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()