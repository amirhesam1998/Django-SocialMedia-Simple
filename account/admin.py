from django.contrib import admin
from .models import Relation , Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User




class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    
class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInLine ,)


admin.site.unregister(User)
admin.site.register(User , ExtendedUserAdmin)
admin.site.register(Relation)