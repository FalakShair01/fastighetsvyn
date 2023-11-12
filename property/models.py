from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
def document_upload(instance, filename):
    return '/'.join(['property', str(instance.property.byggnad), 'documents', filename])

def picture_upload(instance, filename):
    return '/'.join(['property', str(instance.byggnad), 'picture', filename])

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    byggnad = models.CharField(max_length=255)
    fond = models.CharField(max_length=255)
    ansvarig_AM = models.CharField(max_length=255)
    yta = models.IntegerField()
    loa = models.IntegerField()
    bta = models.IntegerField()
    lokal_elproduktion = models.BooleanField()
    installered_effekt = models.IntegerField()
    geo_energi = models.BooleanField()
    epc_tal = models.IntegerField()
    address = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=picture_upload)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.byggnad


class Document(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=document_upload, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)