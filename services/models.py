from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save
from property.models import Property
from users.models import ServiceProvider

User = get_user_model()
# Create your models here.
def service_images(instance, filename):
    return '/'.join(['services', str(instance.title), filename])

class Development(models.Model):    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to=service_images, null=True, blank=True)
    type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class UserDevelopmentServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_development')
    development = models.ForeignKey(Development, on_delete=models.CASCADE, related_name='development_services')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='development_property')
    comment = models.TextField(max_length=255, null=True, blank=True)

    STATUS = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    )

    status = models.CharField(choices=STATUS, max_length=10)
    started_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.status == 'Completed' and not self.end_date:
            self.end_date = timezone.now()
        if self.status == 'Active':
            self.end_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-pk']



# Maintances Services 
class Maintenance(models.Model):    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to=service_images, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class UserMaintenanceServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_maintenance')
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name='maintenance_services')
    # property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='maintaince_property')
    properties = models.ManyToManyField(Property, related_name='maintenance_services', blank=True)  # Changed to ManyToManyField
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, blank=True, null=True, related_name='maintenance_service_provider')
    comment = models.TextField(max_length=255, null=True, blank=True)
    STATUS = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    status = models.CharField(choices=STATUS, max_length=10)
    ITERATIVE = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Other', 'Other'),
    )
    iteration = models.CharField(choices=ITERATIVE, max_length=7, null=True, blank=True)
    day = models.TextField(null=True, blank=True)
    date = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)
    frequency = models.TextField(null=True, blank=True)
    started_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.status == 'Completed' and not self.end_date:
            self.end_date = timezone.now()
        if self.status == 'Active':
            self.end_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-pk']
