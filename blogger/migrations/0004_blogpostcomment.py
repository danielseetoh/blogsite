# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0003_imagedoc'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commenter', models.CharField(max_length=100)),
                ('comment_content', models.CharField(max_length=1000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('blogpost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogger.BlogPost')),
            ],
        ),
    ]