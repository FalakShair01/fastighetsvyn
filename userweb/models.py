from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_miniwebsite_banner(instance, filename):
    return '/'.join(['mini-site', str(instance.user.username), filename])

class Homepage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='home_page')
    banner = models.ImageField(upload_to=upload_miniwebsite_banner)
    title = models.TextField()
    sub_title = models.TextField()
    description = models.TextField()
