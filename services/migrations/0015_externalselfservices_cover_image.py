# Generated by Django 4.2.6 on 2024-11-10 13:26

from django.db import migrations, models
import services.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_alter_ordermaintenanceservices_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalselfservices',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=services.models.exeternal_service_images),
        ),
    ]
