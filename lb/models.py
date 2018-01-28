import datetime
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)
    des = models.CharField(max_length=200)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class User(models.Model):
    name = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    reg_time = models.DateTimeField()
    department = models.CharField(max_length=100)
    website = models.URLField()
    def __str__(self):
        return self.name

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
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Submission(models.Model):
    name = models.CharField(max_length=100)
    des = models.TextField()
    sub_date = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    envir = models.ForeignKey(Environment,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

