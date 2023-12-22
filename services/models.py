from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()
# Create your models here.
def service_images(instance, filename):
    return '/'.join(['services', str(instance.title), filename])

class Development(models.Model):    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to=service_images, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title


class UserDevelopmentServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_development')
    development = models.ForeignKey(Development, on_delete=models.CASCADE, related_name='development_services')
    STATUS = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(choices=STATUS, max_length=10)
    started_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'Completed' and not self.end_date:
            self.end_date = datetime.now()
        super().save(*args, **kwargs)
