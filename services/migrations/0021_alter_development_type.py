# Generated by Django 4.2.6 on 2024-03-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_usermaintenanceservices_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='development',
            name='type',
            field=models.TextField(),
        ),
    ]
