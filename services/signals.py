from .models import UserDevelopmentServices, UserMaintenanceServices
from notifications.models import AdminNotifications
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=UserMaintenanceServices)
def notify_maintenance_to_admin(sender, instance, created, **kwargs):
    if created:
        title = "Underhållstjänstförfrågan"
        description = (
            f"Användare {instance.user.username} begärde en ny underhållstjänst."
        )
        AdminNotifications.objects.create(
            maintenance=instance, title=title, description=description
        )


@receiver(post_save, sender=UserDevelopmentServices)
def notify_development_to_admin(sender, instance, created, **kwargs):
    if created:
        title = "Utvecklingstjänstförfrågan"
        description = (
            f"Användare {instance.user.username} begärde en ny utvecklingstjänst."
        )
        AdminNotifications.objects.create(
            development=instance, title=title, description=description
        )
