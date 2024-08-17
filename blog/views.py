import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .custom_permission import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import BlogSerializer, NewsletterSerializer, NewsLetterSubscriberSerializer
from .models import Blog, Newsletter, NewsLetterSubscriber
from django.conf import settings
from users.Utils import Utils
# from django.contrib.


# Create your views here.

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        blog = serializer.save(user=self.request.user)
        # self.send_blog_notification(blog)
        return serializer

    
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete the associated cover_photo file from the directory
        cover_photo_path = instance.cover_photo.path
        try:
            if cover_photo_path and os.path.exists(cover_photo_path):
                os.remove(cover_photo_path)
        except Exception as e:
            return Response(f"Error deleting cover_photo: {str(e)}")

        # Call the superclass's destroy method to delete the database record
        self.perform_destroy(instance)

        return Response({"detail": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class NewsletterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all().order_by('-created_at')
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class NewsletterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class NewsLetterSubscriberViewset(viewsets.ModelViewSet):
    queryset = NewsLetterSubscriber.objects.all()
    serializer_class = NewsLetterSubscriberSerializer