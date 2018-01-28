from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Submission,Environment,Category

admin.site.register(User,UserAdmin)
admin.site.register(Environment)
admin.site.register(Submission)
admin.site.register(Category)

