# Generated by Django 4.2.6 on 2023-10-28 20:55

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_is_verified_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_to),
        ),
    ]
