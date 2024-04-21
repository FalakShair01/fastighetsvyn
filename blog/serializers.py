from rest_framework import serializers
from .models import Blog, Newsletter, NewsLetterSubscriber
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'description', 'content', 'cover_photo', 'is_sendmail', 'is_sendsms', 'created_at']
    

class TenantBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'description', 'content', 'cover_photo', 'created_at']
    

class NewsletterSerializer(serializers.ModelSerializer):
    creator = UserSerializer(source='author', read_only=True)
    class Meta:
        model = Newsletter
        fields = ['id','author', 'title', 'description', 'content', 'cover_photo', 'created_at', 'creator']
    

class NewsLetterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscriber
        fields = '__all__'