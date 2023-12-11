from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .models import Post , Comment , Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm , CommentCreateForm , CommentReplyForm , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomePage(View):
    template_name = 'home/index.html'
    form_class = PostSearchForm
    
    def get(self,request):
        post = Post.objects.all()
        if request.GET.get('search'):
            post = post.filter(body__contains=request.GET['search'])
        return render(request , self.template_name , {'posts' : post , 'form':self.form_class})
    
    
class PostDetailView(View):
    template_name = 'home/detail.html'
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'] , slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    
    
    def get(self,request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply = False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like= True       
        return render(request , self.template_name , {'post' : self.post_instance , 'comments' : comments , 'form':self.form_class , 'reply_form':self.form_class_reply , 'can_like':can_like})


    @method_decorator(login_required)   #special for login users first
    def post(self,request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request , 'your comment submitted successfully' , 'success')
            return redirect('home:post_detail' , self.post_instance.id , self.post_instance.slug)

class PostDeleteView(LoginRequiredMixin , View):    
    def get(self,request , post_id):
        post = get_object_or_404(Post,pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request ,"post deleted successfully" , 'success')
        else:
            messages.error(request ,"you cant delete this post" , 'danger')
        return redirect('home:homepage')
    
class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update.html'
    
    def setup(self,request,*args,**kwargs):
        '''
        *The main use of this method is to make settings before executing any other method in the view class.
        Typically used for settings related to logins, permissions, or other basic settings.
        ***Its other use is to avoid writing duplicate codes
        ***This method is always used before dispatch method
        '''
        self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self,request,*args,**kwargs):
        '''
        * It is used to identify and select the appropriate method based on the request type and is called before executing any HTTP method (get, post, etc.).
        ** instance = post , show the post body in forms html
        *** commit=False, This allows you to not save an object to the database until it is ensured that all required changes have been made to it or that the information has been filled in correctly.
        **** slugify() , Removes spaces and puts dashes
        '''
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
            
        
        
class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm
    template_name = 'home/create.html'
    
    def get(self,request):
        form = self.form_class
        return render(request , self.template_name , {'form':form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request , 'you post is created' , 'success')
            return redirect('home:post_detail' , new_post.id , new_post.slug)
        messages.error(request , 'your post is not valid' , 'danger')
        return redirect('home:post_create')
    
class PostAddReplyView(LoginRequiredMixin,View):
    form_class = CommentReplyForm
    
    def post(self,request,post_id,comment_id):
        post = get_object_or_404(Post,id=post_id)
        comment = get_object_or_404(Comment , id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request , 'your reply submitted successfully' , 'success')
        return redirect('home:post_detail' , post.id , post.slug)    
            
            
class PostLikeView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        like = Vote.objects.filter(post=post , user = request.user)
        if like.exists():
            messages.error(request , 'you have already liked this post' , 'danger')
        else:
            Vote.objects.create(post=post , user=request.user)
            messages.success(request , 'your liked this post successfully' , 'success')
        return redirect('home:post_detail' , post.id , post.slug)
    
            