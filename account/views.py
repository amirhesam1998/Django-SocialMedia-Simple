from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForms

class RegisterView(View):
    def get(self , request):
        form = UserRegistrationForms()
        return render(request , 'account/register.html' ,{'form' : form})
    
    def post(self,request):
        form = UserRegistrationForms()
        return render(request , 'account/register.html' ,{'form' : form})
