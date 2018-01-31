import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

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
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def save(self, *args, **kwargs):
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        super(User, self).save()
    def get_avatar_url(self):
        url = self.avatar.url
        file_name = url.split('/')[-1]
        if self.socialaccount_set.exists() and file_name == 'default.png':
            url = self.socialaccount_set.first().get_avatar_url()
        return url

@python_2_unicode_compatible
class Environment(models.Model):
    name = models.CharField(max_length=100)
    short_des = models.CharField(max_length=200)
    long_des = RichTextUploadingField()
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
    description = RichTextUploadingField()
    sub_date = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

