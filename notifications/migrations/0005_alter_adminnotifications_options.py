# Generated by Django 4.2.6 on 2024-01-21 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_rename_maintaince_adminnotifications_maintenance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminnotifications',
            options={'ordering': ['-pk']},
        ),
    ]