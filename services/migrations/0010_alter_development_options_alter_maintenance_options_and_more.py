# Generated by Django 4.2.6 on 2023-12-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_userdevelopmentservices_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='development',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='userdevelopmentservices',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='usermaintenanceservices',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='userdevelopmentservices',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], max_length=10),
        ),
        migrations.AlterField(
            model_name='usermaintenanceservices',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Pending', 'Pending'), ('Completed', 'Completed')], max_length=10),
        ),
    ]
