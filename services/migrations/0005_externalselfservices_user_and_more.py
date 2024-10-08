# Generated by Django 4.2.6 on 2024-10-06 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0004_rename_sevicedocument_servicedocument_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalselfservices',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self_services', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='externalselfservices',
            name='kontaktuppgifter_till_ansvarig_leverantor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='self_service_provider', to='services.selfserviceprovider'),
        ),
        migrations.AlterField(
            model_name='externalselfservices',
            name='relevanta_dokument',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='relevanta_dokument', to='services.servicedocumentfolder'),
        ),
    ]
