from django.core.mail import EmailMessage


class Utils:
    @staticmethod
    def send_email(data):
        if isinstance(data["to"], list):
            to_emails = data["to"]
        else:
            to_emails = [data["to"]]

        try:
            email = EmailMessage(
                subject=data["subject"],
                body=data["body"],
                from_email="Support Fastighetsvyn <fastighetsvyn2@gmail.com>",
                to=to_emails,
            )
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            print(f"Sending email Failed : {e}")
