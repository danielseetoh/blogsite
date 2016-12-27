from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django import forms
from django.urls import reverse
from django.db.models import F
from django.views import generic, View
from django.utils import timezone
from .models import *

# Create your views here.

class IndexView(View):
	def get(self, request):
		return render(request, 'blogger/index.html')

class LoginView(View):
	def get(self, request):
		return render(request, 'blogger/login.html')
	def post(self, request):
		usernameval = request.POST['username']
		passwordval = request.POST['password']
		user = authenticate(username=usernameval, password=passwordval)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		else:
			return render(request, 'blogger/login.html', {'error_message': 'Unable to log you in.'})

class SignupView(View):
	def get(self, request):
		return render(request, 'blogger/signup.html')
	def post(self,request):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		blog_title = request.POST['blog_title']
		if Blog.objects.filter(blog_title=blog_title).exists():
			return render(request, 'blogger/signup.html', {'error_message': 'Blog title already exists.'})
		elif User.objects.filter(username=username).exists():
			return render(request, 'blogger/signup.html', {'error_message': 'Username already exists.'})
		else:
			user = User.objects.create_user(username, email, password)
			user.save()
			login(request, user)
			return HttpResponseRedirect(reverse('blogger:blogmanager'))

class BlogView(View):

	def get(self, request):
		context = {}
		if self.request.user.is_authenticated():
			context['username'] = request.user.username
		return render(request, 'blogger/blog.html', context)

@method_decorator(login_required, name='get')
class BlogManagerView(View):
	def get(self, request):
		context = {
			'username': request.user.username
		}
		return render(request, 'blogger/blogmanager.html', context)

@method_decorator(login_required, name='get')
class AccountManagerView(View):
	def get(self, request):
		context = {
			'username': request.user.username
		}
		return render(request, 'blogger/accountmanager.html', context)

@method_decorator(login_required, name='get')
class BlogPostView(View):
	def get(self, request):
		return render(request, 'blogger/blogpost.html')

def logoutView(request):
	logout(request)
	return render(request, 'blogger/index.html')