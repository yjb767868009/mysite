from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
# admin.site.register(Post, PostAdmin)
admin.site.register(Environment)
admin.site.register(Submission)
admin.site.register(Category)

