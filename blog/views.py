from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .custom_permission import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import BlogSerializer, TenantBlogSerializer
from .models import Blog
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, smart_str
from django.conf import settings
from django.urls import reverse
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
        blog_id = blog.id
        user = blog.user
        frontend_domain = settings.FRONTEND_DOMAIN
        uid = urlsafe_base64_encode(force_bytes(user.id))
        url = reverse('blog-notification', args=[uid, blog_id])
        link = frontend_domain + url
        print(link)

        if blog.is_sendmail and blog.is_sendsms:
            
            tenants = user.tenants.all()
            for i in tenants:

                data = {
                    'subject': 'New Blog Notification',
                    'body': f'Hi {i.name}, A new Blog has been Published. Click the link Below to Read it \n\n '+link,
                    'to': i.email
                }
                Utils.send_email(data)

        elif blog.is_sendmail:
            tenants = user.tenants.all()
            for i in tenants:

                data = {
                    'subject': 'New Blog Notification',
                    'body': f'Hi {i.name}, A new Blog has been Published. Click the link Below to Read it \n\n '+link,
                    'to': i.email
                }
                Utils.send_email(data)

        elif blog.is_sendsms:
            pass
        
        return serializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)


class TenantBlogView(APIView):
    def get(self, request, uid, blog_id):
        show_list = request.GET.get('list')
        user = urlsafe_base64_decode(smart_str(uid))
        if show_list:
            blog = Blog.objects.filter(user=user).order_by('-created_at')
            serializer = TenantBlogSerializer(blog, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            blog = Blog.objects.filter(user=user, id=blog_id)
            serializer = TenantBlogSerializer(blog, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)