# Generated by Django 4.2.6 on 2024-01-20 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_adminnotifications_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminnotifications',
            old_name='maintaince',
            new_name='maintenance',
        ),
    ]