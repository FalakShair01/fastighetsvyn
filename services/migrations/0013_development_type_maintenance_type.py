# Generated by Django 4.2.6 on 2024-01-02 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_alter_userdevelopmentservices_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='development',
            name='type',
            field=models.CharField(default='Energy', max_length=255),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='type',
            field=models.CharField(default='Energy', max_length=255),
        ),
    ]
