from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from notifications.models import AdminNotifications

User = get_user_model()


def admin_feeback_image(instance, filename):
    return '/'.join(['feedbacks', 'admin', str(instance.user), filename])

class AdminFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_feedback')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=admin_feeback_image, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=AdminFeedback)
def notify_feedback_to_admin(sender, instance, created, **kwargs):
    if created:
        title = "Ny feedback"
        description = f"En användare, {instance.user.username}, har gett feedback. Kolla in det nu."
        AdminNotifications.objects.create(feedback=instance, title=title, description=description)
        
# class UserFeedback(models.Model):
#     """Feedback that will be given to users(property owner)"""
#     full_name = models.CharField(max_length=50)
