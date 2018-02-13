import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

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
    join_nb =  models.IntegerField(default=0)
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
        return reverse('lb:environment', kwargs={'pk':self.pk})
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
    score = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'submisssion'
        verbose_name_plural = verbose_name
        ordering = ['-score']
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('lb:submission', kwargs={'pk':self.pk})

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
        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True
        return super(EnvironmentCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)


moderator.register(Environment, EnvironmentCommentModerator)

