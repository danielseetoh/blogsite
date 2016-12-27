from django import forms
from django.core import validators

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25)
	password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput)
	email = forms.EmailField(label='Email')
	# need to add in validation here
	blog_title = forms.CharField(label='Blog Title', max_length=50, validators=[validators.validate_slug])

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25)
	password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput)

class BlogPostForm(forms.Form):
	blogpost_title = forms.CharField(label='Blog Title')
	blogpost_text = forms.CharField(label='', widget=forms.Textarea)