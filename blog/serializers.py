from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'description', 'content', 'cover_photo', 'is_sendmail', 'is_sendsms', 'created_at']
    

class TenantBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'description', 'content', 'cover_photo', 'created_at']
    
