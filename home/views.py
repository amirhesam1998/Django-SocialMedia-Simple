from django.shortcuts import render
from django.views import View
from .models import Post

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
