# Generated by Django 4.2.6 on 2024-07-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_tenant_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='property',
        ),
        migrations.AddField(
            model_name='user',
            name='admin_access_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_type',
            field=models.CharField(choices=[('TRIAL', 'Trial'), ('ORIGNAL', 'Orignal')], default='TRIAL', max_length=10),
        ),
    ]