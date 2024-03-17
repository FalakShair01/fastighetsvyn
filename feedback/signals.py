from .models import AdminFeedback
from django.dispatch import receiver
from notifications.models import AdminNotifications
from django.db.models.signals import post_save
from users import Utils

@receiver(post_save, sender=AdminFeedback)
def notify_feedback_to_admin(sender, instance, created, **kwargs):
    if created:
        # Notification to admin
        title = "Ny feedback"
        description = f"En användare, {instance.user.username}, har gett feedback. Kolla in det nu."
        AdminNotifications.objects.create(feedback=instance, title=title, description=description)

        # Email to user
        email_body = f"""
                <p>Hej {instance.user.username}, Tack för din feedback!. Vi återkommer till dig mycket snart!</p>
            """
        data = {
            'subject': 'Tack för din feedback',
            'body': email_body,
            'to': instance.user.email
        }

        Utils.send_email(data)

    elif instance.is_done:  # Check if feedback is marked as done
        # Email to user
        email_body = f"""
                <p>Hej {instance.user.username}, Ditt ärende har blivit löst Tack för din feedback!</p>
                <p></p>
                <p>Tack för din feedback!</p>
            """
        data = {
            'subject': 'Ditt ärende har blivit löst',
            'body': email_body,
            'to': instance.user.email
        }
        Utils.send_email(data)

        