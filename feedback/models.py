from django.db import models
from django.contrib.auth import get_user_model
from users.models import Tenant

User = get_user_model()


def admin_feeback_image(instance, filename):
    return '/'.join(['feedbacks', 'admin', str(instance.user), filename])

def tenant_feedback_image(instance, filename):
    return '/'.join(['feedbacks', 'tenants', str(instance.tenant), filename])


class AdminFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_feedback')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=admin_feeback_image, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TenantsFeedback(models.Model):
    """Feedback that will be given to users(property owner) by Tenants"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks', null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    comment = models.TextField()
    image = models.ImageField(upload_to=tenant_feedback_image, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
