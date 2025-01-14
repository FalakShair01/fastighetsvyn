from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
def document_upload(instance, filename):
    return "/".join(["property", str(instance.folder.name), "documents", filename])


def picture_upload(instance, filename):
    return "/".join(["property", str(instance.gatuadress), "picture", filename])


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    byggnad = models.CharField(max_length=255, null=True, blank=True)
    byggår = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Construction year"
    )
    boarea = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Total living area in building"
    )
    fastighetsbeteckning = models.TextField(null=True, blank=True)
    hiss = models.BooleanField(null=True, blank=True)
    skyddsrum = models.BooleanField(blank=True, null=True)
    antal_våningar = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Number of apartments"
    )
    antal_bostäder = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Number of apartments"
    )
    fjärrvärme = models.BooleanField(blank=True, null=True, default=True)
    solpaneler = models.BooleanField(blank=True, null=True, default=True)
    ventilationssystem = models.TextField(blank=True, null=True)
    uppvärmningssystem = models.TextField(blank=True, null=True)
    postnummer = models.CharField(max_length=255, null=True, blank=True, verbose_name="Postal code")
    gatuadress = models.CharField(max_length=255, null=True, blank=True, verbose_name="Street Address")
    picture = models.ImageField(upload_to=picture_upload, null=True, blank=True)
    longitude = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.byggnad

    def save(self, *args, **kwargs):
        if not self.byggnad:
            self.byggnad = self.gatuadress
        super(Property, self).save(*args, **kwargs)

class Folder(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="folders", null=True
    )
    name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Document(models.Model):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="documents", null=True
    )
    file = models.FileField(upload_to=document_upload, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
