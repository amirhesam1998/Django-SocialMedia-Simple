from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='posts')
    body = models.TextField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',) #ORDER BY ALL OF THE APPLICATIONS
    
    
    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        '''
        send arguments to template url
        '''
        return reverse("home:post_detail", args=(self.id , self.slug))
    
    
    '''
    Post --> User
    p1 = post.objects.first()
    p1.user --> root
    p1.user.email --> a@a.com
    
    
    User --> Post   (_set)
    u1 = User.objects.first()
    u1.post_set.all() =((or))= u1.posts.all() --> show all of post from u1
    u1.post_set.ordering_by('body')
    '''