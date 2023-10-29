from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Blog(models.Model):
    user  = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    cover_photo = models.ImageField(upload_to='blog-cover/', blank=True, null=True)
    content = models.TextField()

    is_sendmail = models.BooleanField(default=False)
    is_sendsms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title