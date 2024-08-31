from django.db import models
# from services.models import UserDevelopmentServices, UserMaintenanceServices
# from feedback.models import AdminFeedback as feedback

# Create your models here.


class AdminNotifications(models.Model):
    development = models.ForeignKey(
        to="services.UserDevelopmentServices",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    maintenance = models.ForeignKey(
        to="services.UserMaintenanceServices",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    feedback = models.ForeignKey(
        to="feedback.AdminFeedback", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-pk"]
