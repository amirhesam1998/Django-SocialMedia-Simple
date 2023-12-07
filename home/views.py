from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render , redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify

class HomePage(View):
    template_name = 'home/index.html'
    
    def get(self,request):
        post = Post.objects.all()
        return render(request , self.template_name , {'posts' : post})
    
    
class PostDetailView(View):
    template_name = 'home/detail.html'
    
    
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id , slug=post_slug)
        return render(request , self.template_name , {'post' : post})


class PostDeleteView(LoginRequiredMixin , View):    
    def get(self,request , post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request ,"post deleted successfully" , 'success')
        else:
            messages.error(request ,"you cant delete this post" , 'danger')
        return redirect('home:homepage')
    
class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateForm
    template_name = 'home/update.html'
    
    def setup(self,request,*args,**kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self,request,*args,**kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request , 'you cant edit this post' , 'danger')
            return redirect('home:homepage')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request , self.template_name , {'form' : form})

    
    def post(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request ,"post edit successfully" , 'success')
            return redirect('home:post_detail' , post.id , post.slug)
            
        