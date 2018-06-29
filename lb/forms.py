from django.forms import ModelForm
from .models import *
from django.db import models
#from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import forms

class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'about','first_name','last_name','signature', 'title','department')

class SubmissionForm(ModelForm):
    checkpoints_file = forms.FileField()
    test_program_file = forms.FileField()
    class Meta:
        model = Submission
        fields = ('name','description','allow_comments')
        # fields = '__all__'

    def __init__(self,environment, user, *args, **kwargs):
        self.owner = user
        self.environment = environment
        super(SubmissionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.owner = self.owner
        self.instance.environment = self.environment
        super(SubmissionForm, self).save(*args, **kwargs)
