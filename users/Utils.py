from django.core.mail import EmailMessage
from django.conf import settings

class Utils():
    @staticmethod
    def send_email(data):
        if isinstance(data['to'], list):
            to_emails = data['to']
        else:
            to_emails = [data['to']]
        
        email = EmailMessage(subject=data['subject'], body=data['body'], from_email='Support Fastighetsvyn <fastighetsvyn2@gmail.com>', to=to_emails)
        email.content_subtype = "html"
        email.send()