# Generated by Django 4.2.6 on 2024-10-21 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_ordermaintenanceservices_communication_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordermaintenanceservices',
            old_name='communication',
            new_name='communication_type',
        ),
        migrations.RenameField(
            model_name='ordermaintenanceservices',
            old_name='contact_email',
            new_name='contact_person_email',
        ),
        migrations.RenameField(
            model_name='ordermaintenanceservices',
            old_name='contact_telephone',
            new_name='contact_person_telephone',
        ),
    ]
