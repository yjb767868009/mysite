from django.forms import ModelForm
from .models import *

class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'about','first_name','last_name','signature', 'title','department')

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ('name','description','score')
        
