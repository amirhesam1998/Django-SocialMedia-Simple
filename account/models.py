from django.db import models

from django.contrib.auth.models import User

class Relation(models.Model):
    '''
    This Model class is for the following section
    '''
    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='followers')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    created = models.DateTimeField(auto_now_add= True)
    
    
    def __str__(self):
        return f'{self.from_user} following {self.to_user}'
    
    
class Profile(models.Model):
    '''
    This Model class is for the profile user ( User class is inherited from Django ready model)    
    '''
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True , blank=True)