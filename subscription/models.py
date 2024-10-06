from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.TextField(null=True, blank=True)
    price_id = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    amount_received = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    customer = models.TextField(null=True, blank=True)
    receipt_email = models.EmailField(null=True, blank=True)
    subscription_expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
