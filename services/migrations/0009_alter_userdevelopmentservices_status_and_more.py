# Generated by Django 4.2.6 on 2023-12-24 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_usermaintenanceservices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevelopmentservices',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], max_length=10),
        ),
        migrations.AlterField(
            model_name='usermaintenanceservices',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], max_length=10),
        ),
    ]
