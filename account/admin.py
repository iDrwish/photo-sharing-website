from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

class UserAdmin(admin.ModelAdmin):
    list_display =  ['user', 'first_name', 'last_name', 'e-mail', 'staff_status']

admin.site.register(Profile,ProfileAdmin)
#admin.site.register(User, UserAdmin)