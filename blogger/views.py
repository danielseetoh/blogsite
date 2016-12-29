from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
from django.urls import reverse
from django.db.models import F
from django.views import generic, View
from django.utils import timezone
from .models import *
from .forms import *

# Create your views here.

def can_access(user, blogpost_id):
	blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
	blog = blogpost.blog
	if user != blog.user:
		return False
	else:
		return True

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
		# context['blog_title'] = blog_title
		blog = get_object_or_404(Blog, pk=blog_title)
		blogposts = blog.blogpost_set.all().order_by('-pub_date')
		context = {
			'blog': blog,
			'blogposts': blogposts
		}
		if self.request.user.is_authenticated():
			context['username'] = request.user.username
		return render(request, 'blogger/blog.html', context)

class BlogPostView(View):
	def get(self, request, blog_title, blogpost_id, blogpost_title):
		blog = get_object_or_404(Blog, pk=blog_title)
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		comment_form = CommentForm(initial={'prev_url': 'blogpost'})
		comments = blogpost.blogpostcomment_set.all()
		if blogpost.blog != blog or blogpost.blogpost_title != blogpost_title:
			return render(request, 'blogger/error.html')
		context = {
			'blog': blog,
			'blogpost': blogpost,
			'comment_form': comment_form,
			'comments': comments,
		}
		image_count = blogpost.imagedoc_set.all().count()
		if image_count>0:
			context['image'] = blogpost.imagedoc_set.all()[image_count-1]
		return render(request, 'blogger/blogpost.html', context)

@method_decorator(login_required, name='get')
class BlogManagerView(View):
	def get(self, request):
		blog = get_object_or_404(Blog, user=request.user)
		blogposts = blog.blogpost_set.all().order_by('-pub_date')
		context = {
			'username': request.user.username,
			'blog': blog,
			'blogposts': blogposts
		}
		return render(request, 'blogger/blogmanager.html', context)

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class AccountManagerView(View):
	def get(self, request):
		blog = get_object_or_404(Blog, user=request.user)
		context = {
			'username': request.user.username,
			'blog': blog,
		}
		return render(request, 'blogger/accountmanager.html', context)
	def post(self, request):
		user = request.user
		if 'delete' in request.POST:
			logout(request)
			user.delete()
			return render(request, 'blogger/index.html')
		return render(request, 'blogger/accountmanager.html')

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class BlogPostCreateView(View):
	def get(self, request):
		form = BlogPostForm()
		context = {
			'username': request.user.username,
			'form': form,
		}
		return render(request, 'blogger/blogpostmanager.html', context)

	def post(self, request):
		form = BlogPostForm(request.POST, request.FILES)
		context = {
			'username': request.user.username,
			'form': form,
		}
		if form.is_valid():
			blog = get_object_or_404(Blog, user=request.user)
			blogpost_title = form.cleaned_data['blogpost_title']
			blogpost_text = form.cleaned_data['blogpost_text']
			blogpost = blog.blogpost_set.create(blogpost_title=blogpost_title, blogpost_text=blogpost_text, pub_date=timezone.now())
			blogpost.save()
			if request.FILES.get('image'):
				image = blogpost.imagedoc_set.create(image=request.FILES['image'])
				image.save()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		return render(request, 'blogger/blogpostmanager.html', context)

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class BlogPostEditView(View):
	def get(self, request, blogpost_id):
		if can_access(request.user, blogpost_id) == False:
			return HttpResponseRedirect(reverse('blogger:error'))
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		form_content = {
			'blogpost_title': blogpost.blogpost_title,
			'blogpost_text': blogpost.blogpost_text,
			
		}
		comments = blogpost.blogpostcomment_set.all()
		comment_form = CommentForm(initial={'prev_url': 'blogpostedit'})
		form = BlogPostForm(form_content)
		context = {
			'username': request.user.username,
			'blogpost': blogpost,
			'form': form,
			'comment_form': comment_form,
			'comments': comments,
		}
		image_count = blogpost.imagedoc_set.all().count()
		if image_count>0:
			context['image'] = blogpost.imagedoc_set.all()[image_count-1]
		return render(request, 'blogger/blogpostmanager.html', context)

	def post(self, request, blogpost_id):
		if can_access(request.user, blogpost_id) == False:
			return HttpResponseRedirect(reverse('blogger:error'))
		form = BlogPostForm(request.POST)
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		context = {
			'username': request.user.username,
			'blogpost': blogpost,
			'form': form,
		}
		if form.is_valid():
			if 'delete' in request.POST:
				blogpost.delete()
				return HttpResponseRedirect(reverse('blogger:blogmanager'))
			blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
			blogpost.blogpost_title = form.cleaned_data['blogpost_title']
			blogpost.blogpost_text = form.cleaned_data['blogpost_text']
			blogpost.save()
			if request.FILES.get('image'):
				image = blogpost.imagedoc_set.create(image=request.FILES['image'])
				image.save()
			return HttpResponseRedirect(reverse('blogger:blogmanager'))
		return render(request, 'blogger/blogpostmanager.html', context)

class ErrorView(View):
	def get(self, request):
		return render(request, 'blogger/error.html')

def logoutView(request):
	logout(request)
	return render(request, 'blogger/index.html')

def addBlogPostComment(request, blog_title, blogpost_id, blogpost_title):
	if request.POST.get('prev_url') == 'blogpost':
		redirect_to = HttpResponseRedirect(reverse('blogger:blogpost', args=[blog_title, blogpost_id, blogpost_title]))
	elif  request.POST.get('prev_url') == 'blogpostedit':
		redirect_to = HttpResponseRedirect(reverse('blogger:blogpostedit', args=[blogpost_id]))
	else:
		return HttpResponseRedirect(reverse('blogger:error'))
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		blogpost = get_object_or_404(BlogPost, pk=blogpost_id)
		if comment_form.is_valid():
			if request.user.username:
				username = request.user.username
			else:
				username = 'Anonymous'
			content = comment_form.cleaned_data['comment']
			blogpostcomment = blogpost.blogpostcomment_set.create(commenter=username, comment_content=content, pub_date=timezone.now())
			blogpostcomment.save()
			return redirect_to
		return redirect_to
	else:
		return redirect_to
