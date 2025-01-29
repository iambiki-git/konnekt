from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'gender', 'phone', 'profile_picture')
