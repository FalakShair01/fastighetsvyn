# Generated by Django 4.2.6 on 2023-12-24 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='ADMIN', max_length=10),
        ),
    ]
