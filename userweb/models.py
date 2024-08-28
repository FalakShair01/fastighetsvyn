from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_miniwebsite_banner(instance, filename):
    return '/'.join(['mini-site', 'banners', str(instance.user.username), filename])

def upload_miniwebsite_document(instance, filename):
    return '/'.join(['mini-site', 'documents', str(instance.user.username), filename])

def upload_miniwebsite_contact_person_image(instance, filename):
    return '/'.join(['mini-site', 'contact-person', str(instance.user.username), filename])

class Homepage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='home_page')
    banner = models.ImageField(upload_to=upload_miniwebsite_banner)
    title = models.TextField()
    sub_title = models.TextField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DocumentPageDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    sub_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Documents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    document = models.FileField(upload_to=upload_miniwebsite_document)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ContactPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to=upload_miniwebsite_contact_person_image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FormLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.TextField()
    button_text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
