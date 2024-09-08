from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.TextField()
    status = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount_received = models.DecimalField(max_digits=15, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=255)
    customer = models.TextField()
    receipt_email = models.EmailField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
