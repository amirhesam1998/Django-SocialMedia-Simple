from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
class UserRegistrationForms(forms.Form):
    '''
    registration form for users
    '''
    username = forms.CharField(widget=forms.TextInput({'class':'form-control'}))            #{'class':'form-control'} this is in bootstrap
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='password' ,widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder' : 'password1'}))
    password2 = forms.CharField(label= 'confirm password', widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder' : ' password2'}))
    
    def clean_email(self):
        '''
        validation email field  (one variable)
        '''
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            raise ValidationError('email already exists')
        return email
    
    def clean_username(self):
        '''
        validation username field (one variable)
        '''
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("username already exists")
        return username
    
    def clean(self):
        '''
        validation password1 and password2 (two variable to gether)
        '''
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'class':'form-control'}))            #{'class':'form-control'} this is in bootstrap
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder' : 'password1'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = Profile
        fields = ('age','bio')