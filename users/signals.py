from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DemoRequests
from django.contrib.auth import get_user_model
from .Utils import Utils
from userweb.models import Homepage

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


# Add Dummy data to every Register user if they their role is User
@receiver(post_save, sender=User)
def fill_dummy_data(sender, instance, created, **kwargs):
    if created:
        if instance.role == "USER" and instance.subscription_type == "TRIAL":
            Homepage.objects.create(
                user=instance,  # Assuming there's a ForeignKey to User
                description="Vi på BRF X strävar efter att skapa en trygg och trivsam boendemiljö för alla våra medlemmar. Här på infosidan hittar du all nödvändig information om våra fastigheter, viktiga meddelanden och kommande aktiviteter. Titta in regelbundet för att hålla dig uppdaterad om allt som rör vår förening och vårt arbete.",
                sub_title="Ditt hem, vårt ansvar – Vi skapar trygghet och trivsel tillsammans.",
                title="Välkommen till BRF X!",
                banner="media/banner.jpg",  # Adjust the path based on where the banner is stored
            )
