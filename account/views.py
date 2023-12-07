from typing import Any
from django import http
from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForms , UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post

class UserRegisterView(View):
    
    form_class = UserRegistrationForms
    template_name = 'account/register.html'
    
    def dispatch(self,request,*args,**kwargs):
        '''
        First, function dispatch is executed before other functions
        '''
        if request.user.is_authenticated:
            return redirect('home:homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name ,{'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password1'])
            messages.success(request , 'your registry is successfully' , 'success')
            return redirect('home:homepage')
        return render(request , self.template_name ,{'form' : form})
    
            
            
class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    
    def dispatch(self,request,*args,**kwargs):
        '''
        First, function dispatch is executed before other functions
        '''
        if request.user.is_authenticated:
            return redirect('home:homepage')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        form = self.form_class()
        return render(request , self.template_name , {'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username=cd['username'] , password=cd['password'])
            if user is not None:
                login(request , user)
                messages.success(request , "you logged in successfully" , "success")
                return redirect('home:homepage')
            messages.error(request , "username or password is wrong" , 'warning')
        return render(request , self.template_name ,{'form' : form})
        

class LogoutView(LoginRequiredMixin,View):
    '''
    
    LoginRequiredMixin This method means that only logged in users can have access
    '''
    def get(self,request):
        logout(request)
        messages.success(request , "logout is successfully", 'success')
        return redirect('home:homepage')
    

class UserProfileView(LoginRequiredMixin,View):
    template_name = 'account/profile.html'
    
    def get(self , request , user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user = user)
        return render(request , self.template_name , {'user':user , 'posts':posts})