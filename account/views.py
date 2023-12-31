from typing import Any
from django import http
from django.shortcuts import render , redirect , get_object_or_404 
from django.views import View
from .forms import UserRegistrationForms , UserLoginForm , EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView , PasswordResetDoneView , PasswordResetConfirmView , PasswordResetCompleteView
from django.urls import reverse_lazy
from .models import Relation 

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
    
    def setup(self,request,*args,**kwargs):
        '''
        A method called setup for the initial settings that receives the next information from the GET request.
        '''
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
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
            user = authenticate(request , username=cd['username'] , password=cd['password'])  #User authentication using username and password input.
            if user is not None:
                login(request , user)
                messages.success(request , "you logged in successfully" , "success")
                if self.next:
                    return redirect(self.next)
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
        is_following = False
        user = get_object_or_404(User,pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request , self.template_name , {'user':user , 'posts':posts , 'is_following':is_following })
    

class UserPasswordRestView(PasswordResetView):
    '''
    Display the email input form (template_name) and move to the next step(success_url) and the contents sent to the email(email_template_name)
    '''
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')  #reverse_lazy == That is, wait until the user enters her email and show her this page
    email_template_name = 'account/password_reset_email.html'         
    
 
   
class UserPasswordRestDoneView(PasswordResetDoneView):
    '''
    Display the message of the success of email sending
    '''
    template_name = 'account/password_reset_done.html'
    
    
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    '''
    Display new passwords form for changes
    '''
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')
    
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    '''
    Display the message for finishing process
    '''
    template_name = 'account/password_reset_complete.html'
    
    
class UserFollowView(LoginRequiredMixin , View):
    '''
    following method ((from_user:request.user(login user) --> to_user:user_following ))
    '''
    def get(self , request , user_id):
        user_following = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user=user_following)
        if relation.exists():
            messages.error(request , "you are already following this user" , 'danger')
        else:
            Relation(from_user = request.user , to_user = user_following).save()
            messages.success(request , "you followed this user" , 'success')
        return redirect('account:user_profile' , user_following.id)

class UserUnfollowView(LoginRequiredMixin , View):
    '''
    unfollowing method ((from_user:request.user(login user) --> to_user:user_unfollowing ))
    '''
    def get(self , request , user_id):
        user_unfollowing = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user=user_unfollowing)
        if relation.exists():
            relation.delete()
            messages.success(request , "you unfollowed this user" , 'success')
        else:
            messages.error(request , "you are not following this user" , 'danger')
        return redirect('account:user_profile' , user_unfollowing.id)

class EditUserView(LoginRequiredMixin,View):
    form_class = EditUserForm
    template_name = 'account/edit_profile.html'
    
    def get(self,request):
        form = self.form_class(instance=request.user.profile , initial={'email':request.user.email})
        '''
        We used instance to show the user's current information inside the form, and we used initial because the email field was not in the profile model,
        but it was there in the EditUserForm form, that's why we couldn't receive the email from the instance.
        '''
        return render(request , self.template_name , {'form':form})
        
    def post(self,request):
        form = self.form_class(request.POST , instance=request.user.profile , initial={'email':request.user.email})
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']  #Email should be saved separately
            request.user.save()
            messages.success(request , 'profile edit successfully' , 'success')
        return redirect('account:user_profile' , request.user.id)