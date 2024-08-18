# Generated by Django 4.2.6 on 2024-08-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_property_latitude_property_longitude'),
        ('services', '0022_alter_usermaintenanceservices_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermaintenanceservices',
            name='property',
        ),
        migrations.AddField(
            model_name='usermaintenanceservices',
            name='properties',
            field=models.ManyToManyField(blank=True, related_name='maintenance_services', to='property.property'),
        ),
    ]
