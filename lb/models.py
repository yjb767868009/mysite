import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)
    des = models.CharField(max_length=200)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class User(AbstractUser):
    signature = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100,blank=True)
    department = models.CharField(max_length=100,blank=True)
    avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/default.png', 
                                 processors=[ResizeToFill(85,85)],)
    def __str__(self):
        return self.username

@python_2_unicode_compatible
class Environment(models.Model):
    name = models.CharField(max_length=100)
    short_des = models.CharField(max_length=200)
    long_des = models.TextField()
    solved = models.CharField(max_length=10)
    passing_line = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    pub_date = models.DateTimeField()
    join_nb =  models.IntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def click_increase(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def get_absolute_url(self):
        return reverse('lb:environment_detail', kwargs={'pk':self.pk})


@python_2_unicode_compatible
class Submission(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    sub_date = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    envir = models.ForeignKey(Environment,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

