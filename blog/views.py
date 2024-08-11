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
from users.models import Tenant
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
        self.send_blog_notification(blog)
        return serializer

    def send_blog_notification(self, blog):
        user = blog.user.username_slug
        username_slug = user.username_slug
        frontend_domain = settings.FRONTEND_DOMAIN
        link = f"{frontend_domain}/website/{username_slug}/blogg"

        if blog.is_sendmail:
            self.send_email_notifications(user, link)

        # Uncomment if SMS functionality is added
        # elif blog.is_sendsms:
        #     self.send_sms_notifications(user, link)

    def send_email_notifications(self, user, link):
        # tenants = user.tenants.all()
        tenants_email_list = Tenant.objects.filter(user=user).values_list('email', flat=True)
        # for tenant in tenants:
        try:
            email_body = f"""
            <html>
                <body>
                    <p>Hej,</p>
                    <p>Vi är glada att informera dig om att en ny blogg har publicerats. Besök vår webbplats och klicka på bloggfliken för att läsa den senaste bloggen.</p>
                    <p>
                        <a href="{link}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Besök vår webbplats</a>
                    </p>
                    <p>Tack för att du valde Fastighetsvyn.</p>
                </body>

            </html>
            """
            data = {
                'body': email_body,
                'subject': "New Blog Notification",
                'to': tenants_email_list,
            }
            Utils.send_email(data)
        except Exception as e:
            # Log the exception
            print(f"Failed to send email to in tenants {tenants_email_list}: {str(e)}")

    # Uncomment if SMS functionality is added
    # def send_sms_notifications(self, user, link):
    #     pass
    
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