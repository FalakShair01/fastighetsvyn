# Generated by Django 4.2.6 on 2024-08-10 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_tenant_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('EXPIRED', 'Expired')], default='ACTIVE', max_length=7),
        ),
    ]
