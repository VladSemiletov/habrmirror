from django.contrib import admin
from userapp.models import User, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)