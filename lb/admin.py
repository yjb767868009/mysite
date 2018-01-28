from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Submission,Environment,Category

admin.site.register(Environment)
admin.site.register(Category)
admin.site.register(User,UserAdmin)
