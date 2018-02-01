from django.forms import ModelForm
from .models import User

class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'signature', 'title','department', 'avatar')
