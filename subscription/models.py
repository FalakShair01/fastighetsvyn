from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('past_due', 'Past Due'),
    )

    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE, null=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    plan = models.CharField(max_length=255, null=True, blank=True)  # Plan name or details
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_trial = models.BooleanField(default=False)
    retry_count = models.IntegerField(default=0)
    max_retries = 3
    plan_name = models.CharField(max_length=255, null=True, blank=True)
    last_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription for {self.user.username} ({'Trial' if self.is_trial else 'Paid'}) - {self.status}"
