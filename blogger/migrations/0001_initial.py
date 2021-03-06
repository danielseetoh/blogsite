# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 09:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_title', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=200)),
                ('post_text', models.CharField(max_length=100000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogger.Blog')),
            ],
        ),
    ]
