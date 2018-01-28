from django.contrib import admin

from .models import User,Submission,Environment,Category

admin.site.register(Environment)
admin.site.register(Category)
