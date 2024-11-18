from django.core.mail import EmailMessage
from django.db import transaction
from django.contrib.auth import get_user_model
from feedback.models import UserFeedback
from blog.models import Blog
from property.models import Property, Folder, Document

User = get_user_model()

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
    
    @staticmethod
    def replicate_dummy_data(user):
        dummy_user_email = "zackaria@kth.se"
        try:
            # Fetch the dummy user
            dummy_user = User.objects.get(email=dummy_user_email)

            with transaction.atomic():
                # Replicate Feedbacks
                dummy_feedbacks = UserFeedback.objects.filter(user=dummy_user)
                feedback_entries = [
                    UserFeedback(
                        user=user,
                        tenant=feedback.tenant,
                        property=feedback.property,
                        full_name=feedback.full_name,
                        email=feedback.email,
                        phone=feedback.phone,
                        comment=feedback.comment,
                        image=feedback.image,
                        is_done=feedback.is_done,
                        is_archive=feedback.is_archive,
                    )
                    for feedback in dummy_feedbacks
                ]
                if feedback_entries:
                    UserFeedback.objects.bulk_create(feedback_entries)

                # Replicate Blogs
                dummy_blogs = Blog.objects.filter(user=dummy_user)
                blog_entries = [
                    Blog(
                        user=user,
                        title=blog.title,
                        description=blog.description,
                        cover_photo=blog.cover_photo,
                        content=blog.content,
                        is_sendmail=blog.is_sendmail,
                        is_sendsms=blog.is_sendsms,
                    )
                    for blog in dummy_blogs
                ]
                if blog_entries:
                    Blog.objects.bulk_create(blog_entries)

                # Replicate Properties
                dummy_properties = Property.objects.filter(user=dummy_user)
                for property_obj in dummy_properties:
                    # Create a copy of the property for the new user
                    new_property = Property.objects.create(
                        user=user,
                        byggnad=property_obj.byggnad,
                        byggår=property_obj.byggår,
                        boarea=property_obj.boarea,
                        fastighetsbeteckning=property_obj.fastighetsbeteckning,
                        hiss=property_obj.hiss,
                        skyddsrum=property_obj.skyddsrum,
                        antal_våningar=property_obj.antal_våningar,
                        antal_bostäder=property_obj.antal_bostäder,
                        fjärrvärme=property_obj.fjärrvärme,
                        solpaneler=property_obj.solpaneler,
                        ventilationssystem=property_obj.ventilationssystem,
                        uppvärmningssystem=property_obj.uppvärmningssystem,
                        postnummer=property_obj.postnummer,
                        gatuadress=property_obj.gatuadress,
                        picture=property_obj.picture,
                        longitude=property_obj.longitude,
                        latitude=property_obj.latitude,
                    )

                    # Replicate Folders for the Property
                    dummy_folders = Folder.objects.filter(property=property_obj)
                    for folder in dummy_folders:
                        new_folder = Folder.objects.create(
                            property=new_property,
                            name=folder.name,
                        )

                        # Replicate Documents for the Folder
                        dummy_documents = Document.objects.filter(folder=folder)
                        document_entries = [
                            Document(
                                folder=new_folder,
                                file=document.file,
                            )
                            for document in dummy_documents
                        ]
                        if document_entries:
                            Document.objects.bulk_create(document_entries)

        except User.DoesNotExist:
            raise ValueError(f"Dummy user with email {dummy_user_email} not found.")
