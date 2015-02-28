from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
	
class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=PasswordInput, max_length=40)
    email = forms.EmailField()
	
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('Username taken.')

class SubmitForm(forms.Form):
    paragraph = forms.CharField(max_length=1000)
    title = forms.CharField(max_length=100)

class HighlightForm(forms.Form):
    highlight = forms.CharField(max_length=1000)

class TagForm(forms.Form):
    image = forms.ImageField()


