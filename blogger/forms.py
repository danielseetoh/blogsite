from django import forms

class SignupForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25)