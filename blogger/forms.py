from django import forms
from django.core import validators

# attributes are declared in the forms, which gives a weird mixing of responsibilities for this file
# there is a better way but requires the download of django-widget-tweaks which separates responsibilities

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
	# need to add in validation here
	blog_title = forms.CharField(label='Blog Title', max_length=50, validators=[validators.validate_slug], widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Password', max_length=25, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class BlogPostForm(forms.Form):
	blogpost_title = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}))
	blogpost_text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}))
	image = forms.ImageField(label='Image', required=False)

class CommentForm(forms.Form):
	comment = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment'}))
	prev_url = forms.CharField(widget=forms.HiddenInput())

class BlogEditForm(forms.Form):
	blog_description = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Description'}), required=False)
	blog_background_color = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Background Color (e.g. red/green/#fff/#123456)'}), required=False)
	blog_banner = forms.ImageField(label='Banner Image', required=False)
