import datetime
import hashlib
import urllib

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django import forms
from ckeditor_uploader.fields import RichTextUploadingField

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django_comments_xtd.moderation import moderator, SpamModerator

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)
    des = models.CharField(max_length=200)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class User(AbstractUser):
    about = RichTextUploadingField(default='',blank=True)
    signature = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100,blank=True)
    department = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def get_absolute_url(self):
        return reverse('lb:account_detail',kwargs={'slug':self.slug})

@python_2_unicode_compatible
class Environment(models.Model):
    name = models.CharField(max_length=100)
    short_des = models.CharField(max_length=200)
    long_des = RichTextUploadingField()
    passing_line = models.IntegerField(default=0)
    category = models.ManyToManyField(Category,blank=True)
    participants = models.ManyToManyField(User,blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    pub_date = models.DateTimeField(default=timezone.now)
    click_count = models.PositiveIntegerField(default=0)
    solved = models.CharField(max_length=20,default="unresolved")
    images = ProcessedImageField(upload_to='environment',
                                 default='environment/default.png', 
                                 processors=[ResizeToFill(100,100)],)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'environment'
        verbose_name_plural = verbose_name
        ordering = ['-pk']

    def click_increase(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def get_absolute_url(self):
        return reverse('lb:environment_discussion', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if len(self.images.name.split('/')) == 1:
            self.image.name = self.name + '/' + self.image.name
        super(Environment, self).save()

    def get_images_url(self):
        url = self.images.url
        file_name = url.split('/')[-1]
        return url

@python_2_unicode_compatible
class Submission(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(default='',blank=True)
    sub_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment,on_delete=models.CASCADE)
    allow_comments = models.BooleanField('allow comments', default=True)
    # score = models.FloatField(max_digits=10, decimal_places=4, default=0)
    score = models.FloatField(default=0.0)

    class Meta:
        verbose_name = 'submisssion'
        verbose_name_plural = verbose_name
        ordering = ['-score']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lb:submission_discussion', kwargs={'pk':self.pk})

    def get_gif_url(self):
        url = '/model/'+self.environment.name+'/'+self.name+'/'+'bestresult.gif'
        return url

class EnvironmentCommentModerator(SpamModerator):
    email_notification = True
    def moderate(self, comment, content_object, request):
        # Make a dictionary where the keys are the words of the message and
        # the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([(clean(w), i)
                    for i, w in enumerate(lowcase_comment.split())])
        return super(EnvironmentCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)


moderator.register(Environment, EnvironmentCommentModerator)

