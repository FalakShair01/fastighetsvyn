from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from property.models import Property
from users.models import ServiceProvider

User = get_user_model()


# Create your models here.
def service_images(instance, filename):
    return "/".join(["services", str(instance.title), filename])

def service_document(instance, filename):
    return "/".join(["services", 'document', filename])

class Development(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to=service_images, null=True, blank=True)
    type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class UserDevelopmentServices(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_development"
    )
    development = models.ForeignKey(
        Development, on_delete=models.CASCADE, related_name="development_services"
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="development_property",
    )
    comment = models.TextField(max_length=255, null=True, blank=True)

    STATUS = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed"),
    )

    status = models.CharField(choices=STATUS, max_length=10)
    started_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == "Completed" and not self.end_date:
            self.end_date = timezone.now()
        if self.status == "Active":
            self.end_date = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-pk"]


# Maintances Services
class Maintenance(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    is_admin = models.BooleanField(default=True)
    image = models.ImageField(upload_to=service_images, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class OrderMaintenanceServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_maintenance")
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name="maintenance_services")
    properties = models.ManyToManyField(Property, related_name="admin_services_properties", blank=True)  # Changed to ManyToManyField
    start_date = models.DateField(null=True, blank=True)
    frequency = models.CharField(max_length=255, null=True, blank=True)
    frequency_clarification = models.TextField(null=True, blank=True)
    access_details = models.TextField(null=True, blank=True)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_telephone = models.CharField(max_length=255, null=True, blank=True)
    contact_person_email = models.EmailField(null=True, blank=True)
    communication_type = models.CharField(max_length=255, null=True, blank=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, blank=True, null=True, related_name="maintenance_service_provider",)
    STATUS = (
        ("Active", "Active"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    )
    status = models.CharField(choices=STATUS, max_length=10, default="Pending")
    comment = models.TextField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == "Completed" and not self.end_date:
            self.end_date = timezone.now().date()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-pk"]


class OrderServiceDocumentFolder(models.Model):
    order_service = models.ForeignKey(
        OrderMaintenanceServices, on_delete=models.CASCADE, related_name="documents_folder", null=True
    )
    name = models.CharField(max_length=50, default='Dokument')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OrderServiceFile(models.Model):
    folder = models.ForeignKey(
        OrderServiceDocumentFolder, on_delete=models.CASCADE, related_name="documents", null=True
    )  
    file = models.FileField(upload_to=service_document, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document in {self.folder.name}"

class SelfServiceProvider(models.Model):
    foretag = models.TextField()  # Company
    namn = models.CharField(max_length=255)  # Name
    telefon = models.CharField(max_length=255)  # Phone
    e_post = models.EmailField()  # Email
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.namn} ({self.foretag})"

class ExternalSelfServices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='self_services', null=True)
    benamning_av_tjanst = models.CharField(max_length=255)  # Service name
    kostnad_per_manad = models.CharField(max_length=255)  # Monthly cost
    vilka_byggnader_omfattas = models.ManyToManyField(Property, related_name='self_service_properties')  # Related properties
    beskrivning = models.TextField(null=True, blank=True)  # Description
    startdatum_for_underhallstjanst = models.DateField(null=True, blank=True)  # Start date
    hur_ofta_utfor_denna_tjanst = models.CharField(max_length=255, null=True, blank=True)  # Service frequency
    fortydligande_av_tjanstens_frekvens = models.TextField(null=True, blank=True)  # Frequency clarification
    access = models.TextField(null=True, blank=True)  # Access details
    kontaktuppgifter_till_ansvarig_leverantor = models.ForeignKey(
        SelfServiceProvider, on_delete=models.SET_NULL, null=True, related_name="self_service_provider"
    )  # Service provider
    anteckningar = models.TextField(null=True, blank=True)  # Notes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.benamning_av_tjanst

class ServiceDocumentFolder(models.Model):
    manual_service = models.ForeignKey(
        ExternalSelfServices, on_delete=models.CASCADE, related_name="documents_folder", null=True
    )
    name = models.CharField(max_length=50, default='Dokument')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ServiceFile(models.Model):
    folder = models.ForeignKey(
        ServiceDocumentFolder, on_delete=models.CASCADE, related_name="documents", null=True
    )  
    file = models.FileField(upload_to=service_document, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document in {self.folder.name}"