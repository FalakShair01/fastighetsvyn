# Generated by Django 4.2.6 on 2024-10-08 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_rename_external_self_service_servicedocumentfolder_manual_service'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServiceDocument',
            new_name='ServiceFile',
        ),
    ]
