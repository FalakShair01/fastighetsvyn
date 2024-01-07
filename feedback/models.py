from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def admin_feeback_image(instance, filename):
    return '/'.join(['feedbacks', 'admin', str(instance.user), filename])

class AdminFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_feedback')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to=admin_feeback_image, null=True, blank=True)