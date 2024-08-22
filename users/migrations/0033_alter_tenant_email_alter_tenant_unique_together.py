# Generated by Django 4.2.6 on 2024-08-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_alter_tenant_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterUniqueTogether(
            name='tenant',
            unique_together={('user', 'email')},
        ),
    ]