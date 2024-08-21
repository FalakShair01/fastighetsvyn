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
        # Check if cover_photo is associated with the instance
        cover_photo = instance.cover_photo
        if cover_photo and hasattr(cover_photo, 'path'):
            cover_photo_path = cover_photo.path
            try:
                if os.path.exists(cover_photo_path):
                    os.remove(cover_photo_path)
            except Exception as e:
                return Response({"error": f"Error deleting cover_photo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Call the superclass's destroy method to delete the database record
        self.perform_destroy(instance)

        return Response({"detail": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
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