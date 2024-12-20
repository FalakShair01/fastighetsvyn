# Generated by Django 4.2.6 on 2024-11-16 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_subscription_price_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subscription_type',
            field=models.CharField(choices=[('Trial', 'Trial'), ('Paid', 'Paid')], default='Trial', max_length=5),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='amount_received',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
