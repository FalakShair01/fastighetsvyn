# Generated by Django 4.2.6 on 2023-10-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_is_sendmail_blog_is_sendsms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_sendmail',
            field=models.BooleanField(default=False),
        ),
    ]