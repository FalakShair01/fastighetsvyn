# Generated by Django 4.2.6 on 2024-03-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='phone',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
