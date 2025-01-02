from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DemoRequests
from django.contrib.auth import get_user_model
from .Utils import Utils
from userweb.models import Homepage
from subscription.models import Subscription
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

@receiver(post_save, sender=DemoRequests)
def send_demo_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        admins_emails = User.objects.filter(role="ADMIN").values_list(
            "email", flat=True
        )
        subject = "Ny Demo-begäran"
        body = """
            <html>
                <body>
                    <p>Hej admin,</p>
                    <p>En ny demo-begäran har skickats in med denna e-postadress:</p>
                    <p><b>Email:</b> {}</p>
                    <p>Vänligen lägg till användaren i instrumentpanelen för att ge dem demotillgång.</p>
                </body>
            </html>
        """.format(email)
        data = {"subject": subject, "body": body, "to": list(admins_emails)}
        Utils.send_email(data)

@receiver(post_save, sender=User)
def create_trial_subscription(sender, instance, created, **kwargs):
    if created:
        if instance.role == "USER":
            # Calculate end date
            end_date=timezone.now() + timedelta(days=settings.TRIAL_DURATION)
            
            # Create trial subscription
            Subscription.objects.create(
                user=instance,
                is_trial=True,
                status='active',
                start_date=timezone.now(),
                end_date=end_date,
            )
            
            # Update user's subscription expiry
            instance.subscription_expiry = end_date
            instance.save(update_fields=["subscription_expiry"])

# Add Dummy data to every Register user if they their role is User
@receiver(post_save, sender=User)
def fill_dummy_data(sender, instance, created, **kwargs):
    """
        This function will populate initial data for a newly registered user.
        
        - It will create dummy data on the mini web for the user.
        - It will set up a trial subscription for the user.
    """
    try: 
        if created:
            if instance.role == "USER":
                # mini website data
                Homepage.objects.create(
                    user=instance,  # Assuming there's a ForeignKey to User
                    description="Vi på BRF X strävar efter att skapa en trygg och trivsam boendemiljö för alla våra medlemmar. Här på infosidan hittar du all nödvändig information om våra fastigheter, viktiga meddelanden och kommande aktiviteter. Titta in regelbundet för att hålla dig uppdaterad om allt som rör vår förening och vårt arbete.",
                    sub_title="Ditt hem, vårt ansvar – Vi skapar trygghet och trivsel tillsammans.",
                    title="Välkommen till BRF X!",
                    banner='mini-web-common-banner.jpeg'
                )
    except Exception as e:
        print(f"error in new register user data creation: {e}")

# @receiver(post_save, sender=User)
# def update_subscription_on_user_change(sender, instance, **kwargs):
#     # Check if subscription_expiry is set
#     if instance.subscription_expiry:
#         # Update all related subscriptions
#         subscriptions = Subscription.objects.filter(user=instance)
#         for subscription in subscriptions:
#             # Update `end_date` in Subscription table
#             subscription.end_date = instance.subscription_expiry
            
#             # Update `status` in Subscription table
#             if instance.subscription_expiry > timezone.now():
#                 subscription.status = 'active'
#             else:
#                 subscription.status = 'expired'
            
#             subscription.save()

#         # Update `subscription_status` in User table
#         if instance.subscription_expiry > timezone.now():
#             instance.subscription_status = "ACTIVE"
#         else:
#             instance.subscription_status = "EXPIRED"
#         instance.save(update_fields=['subscription_status'])

@receiver(post_save, sender=User)
def update_subscription_on_user_change(sender, instance, **kwargs):
    # Use a flag to prevent infinite recursion
    if hasattr(instance, '_updating_subscription'):
        return

    if instance.subscription_expiry:
        subscriptions = Subscription.objects.filter(user=instance)
        for subscription in subscriptions:
            subscription.end_date = instance.subscription_expiry

            # Update `status` in Subscription table
            subscription.status = 'active' if instance.subscription_expiry > timezone.now() else 'expired'
            subscription.save()

        # Update `subscription_status` in User table
        instance._updating_subscription = True  # Set the flag
        try:
            instance.subscription_status = "ACTIVE" if instance.subscription_expiry > timezone.now() else "EXPIRED"
            instance.save(update_fields=['subscription_status'])
        finally:
            del instance._updating_subscription  # Remove the flag