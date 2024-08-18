# Generated by Django 4.2.6 on 2024-08-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_user_subscription_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
    ]