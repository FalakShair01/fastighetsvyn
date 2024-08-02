from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Homepage, DocumentPageDetail, Documents
from .serializers import HomePageSerializer, DocumentPageDetailSerializer, DocumentSerializer, ContactUsFormSerializer
from users.models import User
from users.Utils import Utils
from blog.models import Blog
from blog.serializers import TenantBlogSerializer
from django.shortcuts import get_object_or_404

class HomepageView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        homepage_detail = Homepage.objects.filter(user=user)
        serializer = HomePageSerializer(homepage_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HomePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, username_slug, pk):
        user = User.objects.get(username_slug=username_slug)
        instance = Homepage.objects.get(id=pk, user=user)
        serializer = HomePageSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
 
class ListUserBlogView(APIView):

    def get(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        blogs = Blog.objects.filter(user=user)
        serializer = TenantBlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUserBlogView(APIView):

    def get(self, request, username_slug, pk):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        blogs = get_object_or_404(Blog, id=pk , user=user)
        serializer = TenantBlogSerializer(blogs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentPageDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        document_detail = DocumentPageDetail.objects.filter(user=user)
        serializer = DocumentPageDetailSerializer(document_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DocumentPageDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DocumentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        document = Documents.objects.filter(user=user)
        serializer = DocumentSerializer(document, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ContactPageView(APIView):
    def post(self, request, username_slug):
        user = get_object_or_404(User, username_slug=username_slug)
        to_email = user.email
        serializer = ContactUsFormSerializer(data=request.data)
        if serializer.is_valid():
            sender_name = serializer.validated_data['name']     
            sender_phone = serializer.validated_data['phone']     
            sender_email = serializer.validated_data['email']     
            sender_message = serializer.validated_data['message']

            email_body = f"""
                <h2>Ny kontaktformulärsinlämning</h2>
                <p><strong>Namn:</strong> {sender_name}</p>
                <p><strong>Telefon:</strong> {sender_phone}</p>
                <p><strong>E-post:</strong> {sender_email}</p>
                <p><strong>Meddelande:</strong><br>{sender_message}</p>
            """

            email_data = {
                'subject': f"Ny kontaktformulärsinlämning från {sender_name}",
                'body': email_body,
                'to': user.email
            }

            Utils.send_email(email_data)
            return Response({'message': 'Form submitted successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)