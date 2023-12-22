# Generated by Django 4.2.6 on 2023-12-22 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import services.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='development',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='development',
            name='started_date',
        ),
        migrations.RemoveField(
            model_name='development',
            name='status',
        ),
        migrations.AddField(
            model_name='development',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=services.models.service_images),
        ),
        migrations.CreateModel(
            name='UserDevelopmentServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('COMPLETED', 'Completed')], max_length=10)),
                ('started_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('development', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='development_services', to='services.development')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_development', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
