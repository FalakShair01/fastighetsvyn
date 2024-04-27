from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DemoRequests, ContactUs
from django.contrib.auth import get_user_model
from .Utils import Utils

User = get_user_model()

@receiver(post_save, sender=DemoRequests)
def send_demo_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        admins_emails = User.objects.filter(role='ADMIN').values_list('email', flat=True)
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
        data = {'subject': subject, 'body': body, 'to': list(admins_emails)}
        Utils.send_email(data)


@receiver(post_save, sender=ContactUs)
def send_contact_us_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        phone = instance.phone  
        message = instance.message
        admins_emails = User.objects.filter(role='ADMIN').values_list('email', flat=True)
        subject = "Ny Kontakta oss-förfrågan"
        body = """
            <html>
                <body>
                    <p>Hej Admin,</p>
                    <p>En ny förfrågan har skickats in med följande uppgifter:</p>
                    <p><b>E-post:</b> {email}</p>
                    <p><b>Telefonnummer:</b> {phone}</p>
                    <p><b>Meddelande:</b> {message}</p>
                    <p>Vänligen granska och svara enligt behov.</p>
                </body>
            </html>
        """.format(email=email, phone=phone, message=message)
        data = {'subject': subject, 'body': body, 'to': list(admins_emails)}
        Utils.send_email(data)