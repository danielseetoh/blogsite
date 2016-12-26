from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

# class Blog(models.Model):
# 	blog_title = models.CharField(max_length=100)
# 	pub_date = modelx.DateTimeField('date published')

# 	def __str__(self):
# 		return self.blog_title

# class Post(models.Model):
# 	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
# 	post_title = models.CharField(max_length=200)
# 	post_text = models.CharField(max_length=100000)

# 	#images?

# 	def __str__(self):
# 		return self.post_title

