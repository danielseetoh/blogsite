from django.conf.urls import url
from . import views

app_name = 'blogger'

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
	url(r'^signup$', views.SignupView.as_view(), name='signup'),
	url(r'^blog/([a-zA-Z0-9_]+)$', views.BlogView.as_view(), name='blog'),
	url(r'^blogmanager$', views.BlogManagerView.as_view(), name='blogmanager'),
	url(r'^accountmanager$', views.AccountManagerView.as_view(), name='accountmanager'),
	url(r'^blogpostcreate$', views.BlogPostCreateView.as_view(), name='blogpostcreate'),
	url(r'^blogpostedit/(?P<blogpost_id>[0-9]+)$', views.BlogPostEditView.as_view(), name='blogpostedit'),
	url(r'^logout$', views.logoutView, name='logout'),
	
]