# Generated by Django 4.2.6 on 2024-08-31 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username_slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]