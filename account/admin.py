from django.contrib import admin
from .models import Relation , Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User




class ProfileInLine(admin.StackedInline):
    '''
    This inline enables the display of profile information on the user's edit page.
    '''
    model = Profile
    can_delete = False
    
class ExtendedUserAdmin(UserAdmin):
    '''
    This will make the user's editing form also display the information related to the Profile.
    '''
    inlines = (ProfileInLine ,)


admin.site.unregister(User)
'''
With this command, it first removes the user from its management at least.
'''
admin.site.register(User , ExtendedUserAdmin)
'''
Here, the customized ExtendedUserAdmin class is added back to User.
This will make the user management appear in the management panel, with the new changes we have added (profile information display in the user form).
'''
admin.site.register(Relation)