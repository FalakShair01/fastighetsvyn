from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
def blog_cover(instance, filename):
    return '/'.join(['blog-cover', str(instance.title), filename])

def newsletter_cover(instance, filename):
    return '/'.join(['newsletter_cover', str(instance.title), filename])

class Blog(models.Model):
    user  = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to=blog_cover, blank=True, null=True)
    content = models.TextField()
    is_sendmail = models.BooleanField(default=False)
    is_sendsms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Newsletter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletter')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    cover_photo = models.ImageField(upload_to=newsletter_cover, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewsLetterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
