# Generated by Django 4.2.6 on 2024-03-12 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_managers_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='managers',
            old_name='full_name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='managers',
            name='role',
            field=models.CharField(default='Manager', max_length=7),
        ),
    ]
