from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Newsletter, NewsLetterSubscriber
from users.Utils import Utils
from django.urls import reverse
from django.conf import settings  # Add this import


@receiver(post_save, sender=Newsletter)
def send_newsletter_notification(sender, instance, created, **kwargs):
    if created:
        newsletter_title = instance.title
        newsletter_url = settings.FRONTEND_DOMAIN + reverse('newsletter-detail', kwargs={'pk': instance.pk})
        subscribers_emails = NewsLetterSubscriber.objects.all().values_list('email', flat=True)
        
        subject = "Ny Nyhetsbrev Publicerad: {}".format(newsletter_title)
        body = """
            <html>
                <body>
                    <p>Hej,</p>
                    <p>Ett nytt nyhetsbrev med titeln '{}' har publicerats.</p>
                    <p>Klicka <a href="{}">här</a> för att läsa mer.</p>
                    <p>Tack.</p>
                </body>
            </html>
        """.format(newsletter_title, newsletter_url)
        
        data = {'subject': subject, 'body': body, 'to': list(subscribers_emails)}
        Utils.send_email(data)