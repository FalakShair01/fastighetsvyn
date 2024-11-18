from django.core.mail import EmailMessage
from django.db import transaction
from django.contrib.auth import get_user_model
from economi.models import Expense
from feedback.models import UserFeedback
from blog.models import Blog
from property.models import Property, Folder, Document
from services.models import ExternalSelfServices, OrderMaintenanceServices, OrderServiceDocumentFolder, OrderServiceFile, ServiceDocumentFolder, ServiceFile
from .models import Tenant
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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
        """
        Replicates dummy data from a predefined dummy user to the specified user.
        
        Args:
            user (User): The target user to replicate the data for.
        """
        dummy_user_email = settings.DUMMY_ACCOUNT_EMAIL
        try:
            # Fetch the dummy user
            dummy_user = User.objects.get(email=dummy_user_email)

            with transaction.atomic():
                # Initialize a property map for associating tenants with new properties
                property_map = {}

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
                    property_map[property_obj.id] = new_property

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

                # Replicate Tenants
                dummy_tenants = Tenant.objects.filter(user=dummy_user)
                tenant_entries = []
                for tenant in dummy_tenants:
                    # Associate replicated property, if applicable
                    replicated_property = (
                        property_map.get(tenant.property.id) if tenant.property else None
                    )
                    tenant_entries.append(
                        Tenant(
                            user=user,
                            name=tenant.name,
                            property=replicated_property,
                            appartment_no=tenant.appartment_no,
                            email=tenant.email,
                            phone=tenant.phone,
                            profile=tenant.profile,
                            comment=tenant.comment,
                        )
                    )
                if tenant_entries:
                    Tenant.objects.bulk_create(tenant_entries)
                
                # Replicate Expenses
                dummy_expenses = Expense.objects.filter(user=dummy_user)
                expense_entries = []
                for expense in dummy_expenses:
                    # Associate replicated property with the expense, if applicable
                    replicated_property = (
                        property_map.get(expense.building.id) if expense.building else None
                    )
                    expense_entries.append(
                        Expense(
                            user=user,
                            type_of_transaction=expense.type_of_transaction,
                            type_of_cost_or_revenue=expense.type_of_cost_or_revenue,
                            date_of_transaction=expense.date_of_transaction,
                            total_sum=expense.total_sum,
                            value_added_tax=expense.value_added_tax,
                            account=expense.account,
                            building=replicated_property,
                            comment=expense.comment,
                            attachment=expense.attachment,
                        )
                    )
                if expense_entries:
                    Expense.objects.bulk_create(expense_entries)
                

                # Replicate Order Maintenance Services
                dummy_maintenance_orders = OrderMaintenanceServices.objects.filter(user=dummy_user)
                maintenance_entries = []
                for order in dummy_maintenance_orders:
                    # Replicate ManyToManyField properties
                    associated_properties = [property_map.get(prop.id) for prop in order.properties.all()]
                    new_order = OrderMaintenanceServices.objects.create(
                        user=user,
                        maintenance=order.maintenance,
                        start_date=order.start_date,
                        frequency=order.frequency,
                        frequency_clarification=order.frequency_clarification,
                        access_details=order.access_details,
                        contact_person_name=order.contact_person_name,
                        contact_person_telephone=order.contact_person_telephone,
                        contact_person_email=order.contact_person_email,
                        communication_type=order.communication_type,
                        service_provider=order.service_provider,
                        status=order.status,
                        comment=order.comment,
                        end_date=order.end_date,
                    )
                    new_order.properties.set(associated_properties)
                    maintenance_entries.append(new_order)

                # Replicate Order Service Folders and Files
                for order in maintenance_entries:
                    dummy_folders = OrderServiceDocumentFolder.objects.filter(order_service=order)
                    for folder in dummy_folders:
                        new_folder = OrderServiceDocumentFolder.objects.create(
                            order_service=order,
                            name=folder.name,
                        )
                        dummy_files = OrderServiceFile.objects.filter(folder=folder)
                        file_entries = [
                            OrderServiceFile(folder=new_folder, file=file.file)
                            for file in dummy_files
                        ]
                        if file_entries:
                            OrderServiceFile.objects.bulk_create(file_entries)

                # Replicate External Self Services
                dummy_self_services = ExternalSelfServices.objects.filter(user=dummy_user)
                self_service_entries = []
                for service in dummy_self_services:
                    associated_properties = [property_map.get(prop.id) for prop in service.vilka_byggnader_omfattas.all()]
                    new_service = ExternalSelfServices.objects.create(
                        user=user,
                        benamning_av_tjanst=service.benamning_av_tjanst,
                        kostnad_per_manad=service.kostnad_per_manad,
                        beskrivning=service.beskrivning,
                        startdatum_for_underhallstjanst=service.startdatum_for_underhallstjanst,
                        hur_ofta_utfor_denna_tjanst=service.hur_ofta_utfor_denna_tjanst,
                        fortydligande_av_tjanstens_frekvens=service.fortydligande_av_tjanstens_frekvens,
                        access=service.access,
                        kontaktuppgifter_till_ansvarig_leverantor=service.kontaktuppgifter_till_ansvarig_leverantor,
                        anteckningar=service.anteckningar,
                        cover_image=service.cover_image,
                    )
                    new_service.vilka_byggnader_omfattas.set(associated_properties)
                    self_service_entries.append(new_service)

                # Replicate Service Folders and Files
                for service in self_service_entries:
                    dummy_folders = ServiceDocumentFolder.objects.filter(manual_service=service)
                    for folder in dummy_folders:
                        new_folder = ServiceDocumentFolder.objects.create(
                            manual_service=service,
                            name=folder.name,
                        )
                        dummy_files = ServiceFile.objects.filter(folder=folder)
                        file_entries = [
                            ServiceFile(folder=new_folder, file=file.file)
                            for file in dummy_files
                        ]
                        if file_entries:
                            ServiceFile.objects.bulk_create(file_entries)

        except ObjectDoesNotExist:
            raise ValueError(f"Dummy user with email {dummy_user_email} not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while replicating data: {e}")