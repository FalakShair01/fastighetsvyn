# Generated by Django 4.2.6 on 2024-03-30 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0021_alter_development_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermaintenanceservices',
            name='date',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermaintenanceservices',
            name='day',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermaintenanceservices',
            name='time',
            field=models.TextField(blank=True, null=True),
        ),
    ]