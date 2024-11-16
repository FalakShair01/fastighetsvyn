# Generated by Django 4.2.6 on 2024-11-16 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscription', '0005_rename_payment_id_subscription__id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='subscription_expiry',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='subscription',
            old_name='currency',
            new_name='plan',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='_id',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='amount_received',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='receipt_email',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='subscription_type',
        ),
        migrations.AddField(
            model_name='subscription',
            name='is_trial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='last_payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='retry_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('pending', 'Pending'), ('past_due', 'Past Due')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]
