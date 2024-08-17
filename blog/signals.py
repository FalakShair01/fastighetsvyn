from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Newsletter, NewsLetterSubscriber, Blog
from users.models import Tenant
from users.Utils import Utils
from django.urls import reverse
from django.conf import settings  # Add this import


@receiver(post_save, sender=Blog)
def send_blog_notification(sender, instance, created, **kwargs):
    user = instance.user.username_slug
    blog_title = instance.title
    username_slug = user.username_slug
    frontend_domain = settings.FRONTEND_DOMAIN
    link = f"{frontend_domain}/website/{username_slug}/blogg"

    if instance.is_sendmail:
        send_email_notifications(user, link, blog_title)

    # Uncomment if SMS functionality is added
    # elif blog.is_sendsms:
    #     self.send_sms_notifications(user, link)

def send_email_notifications(user, link, blog_title):
    # tenants = user.tenants.all()
    tenants_email_list = Tenant.objects.filter(user=user).values_list('email', flat=True)
    # for tenant in tenants:
    try:
        email_body = f"""
        <html>
            <body>
                <p>Hej,</p>
                <p>Vi är glada att meddela att en ny blogg har publicerats.</p>
                <p>Klicka på knappen nedan för att läsa hela blogginlägget:</p>
                <a href="{ link }" class="button">Läs Blogg</a>
                <p>Tack för att du följer oss!</p>
            </body>

        </html>
        """
        data = {
            'body': email_body,
            'subject': blog_title,
            'to': tenants_email_list,
        }
        Utils.send_email(data)
    except Exception as e:
        # Log the exception
        print(f"Failed to send email to in tenants {tenants_email_list}: {str(e)}")

# Uncomment if SMS functionality is added
# def send_sms_notifications(self, user, link):
#     pass

@receiver(post_save, sender=Newsletter)
def send_newsletter_notification(sender, instance, created, **kwargs):
    if created:
        newsletter_title = instance.title
        newsletter_url = settings.FRONTEND_DOMAIN
        subscribers_emails = NewsLetterSubscriber.objects.all().values_list('email', flat=True)
        
        subject = newsletter_title
        body = f"""
            <html>
                <body>
                    <p>Hej,</p>
                    <p>Ett nytt nyhetsbrev har publicerats.</p>
                    <p>Klicka på knappen nedan för att läsa mer:</p>
                    <a href={ newsletter_url } class="button">Läs Nyhetsbrevet</a>
                    <p>Tack för att du följer oss!</p>
                </body>
            </html>
        """
        
        data = {'subject': subject, 'body': body, 'to': list(subscribers_emails)}
        Utils.send_email(data)