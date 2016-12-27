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
from .forms import *

# Create your views here.

class IndexView(View):
	def get(self, request):
		return render(request, 'blogger/index.html')

class LoginView(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'blogger/login.html', {'form': form})
	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('blogger:blogmanager'))
			else:
				return render(request, 'blogger/login.html', {'error_message': 'Unable to log you in.', 'form': form})
		return render(request, 'blogger/login.html', {'form': form})

class SignupView(View):
	def get(self, request):
		form = SignupForm()
		return render(request, 'blogger/signup.html', {'form': form})
	def post(self,request):
		# add some checks to ensure fields are filled up
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			blog_title = form.cleaned_data['blog_title']
			if Blog.objects.filter(blog_title=blog_title).exists():
				return render(request, 'blogger/signup.html', {'error_message': 'Blog title already exists', 'form': form})
			elif User.objects.filter(username=username).exists():
				return render(request, 'blogger/signup.html', {'error_message': 'Username already exists', 'form': form})
			else:
				user = User.objects.create_user(username, email, password)
				user.save()
				login(request, user)
				blog = Blog(blog_title=blog_title, pub_date=timezone.now(), user=request.user)
				blog.save()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		return render(request, 'blogger/signup.html', {'form': form})

class BlogView(View):
	def get(self, request, blog_title):
		context = {}
		# context['blog_title'] = blog_title
		blog = get_object_or_404(Blog, pk=blog_title)
		context['blog'] = blog
		if self.request.user.is_authenticated():
			context['username'] = request.user.username
		return render(request, 'blogger/blog.html', context)

@method_decorator(login_required, name='get')
class BlogManagerView(View):
	def get(self, request):
		blog = get_object_or_404(Blog, user=request.user)
		context = {
			'username': request.user.username,
			'blog': blog,
		}
		return render(request, 'blogger/blogmanager.html', context)

@method_decorator(login_required, name='get')
class AccountManagerView(View):
	def get(self, request):
		blog = get_object_or_404(Blog, user=request.user)
		context = {
			'username': request.user.username,
			'blog': blog,
		}
		return render(request, 'blogger/accountmanager.html', context)

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class BlogPostCreateView(View):
	def get(self, request):
		form = BlogPostForm()
		context = {
			'username': request.user.username,
			'form': form,
		}
		return render(request, 'blogger/blogpost.html', context)

	def post(self, request):
		form = BlogPostForm(request.POST)
		if form.is_valid():
			blog = get_object_or_404(Blog, user=request.user)
			blogpost_title = form.cleaned_data['blogpost_title']
			blogpost_text = form.cleaned_data['blogpost_text']
			blogpost = blog.blogpost_set.create(blogpost_title=blogpost_title, blogpost_text=blogpost_text, pub_date=timezone.now())
			blogpost.save()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		return render(request, 'blogger/blogpost.html', context)

@method_decorator(login_required, name='get')
class BlogPostEditView(View):
	def get(self, request, blogpost_id):
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		form_content = {
			'blogpost_title': blogpost.blogpost_title,
			'blogpost_text': blogpost.blogpost_text,
		}
		form = BlogPostForm(form_content)
		context = {
			'username': request.user.username,
			'blogpost': blogpost,
			'form': form,
		}
		return render(request, 'blogger/blogpost.html', context)
	def post(self, request, blogpost_id):
		form = BlogPostForm(request.POST)
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		context = {
			'username': request.user.username,
			'blogpost': blogpost,
			'form': form,
		}
		if 'delete' in request.POST:
			blogpost.delete()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		if form.is_valid():
			blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
			blogpost.blogpost_title = form.cleaned_data['blogpost_title']
			blogpost.blogpost_text = form.cleaned_data['blogpost_text']
			blogpost.save()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		return render(request, 'blogger/blogpost.html', context)

def logoutView(request):
	logout(request)
	return render(request, 'blogger/index.html')