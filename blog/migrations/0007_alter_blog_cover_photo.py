# Generated by Django 4.2.6 on 2023-11-11 16:58

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blog_is_sendmail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.blog_cover),
        ),
    ]