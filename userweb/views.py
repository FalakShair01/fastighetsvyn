from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Homepage, DocumentPageDetail, Documents, ContactPerson, FormLinks
from .serializers import (HomePageSerializer, DocumentPageDetailSerializer, DocumentSerializer, 
                          ContactUsFormSerializer, ContactPersonSerializer, FormLinksSerializer)
from users.models import User
from users.Utils import Utils
from blog.models import Blog
from blog.serializers import BlogSerializer
from users.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404

# HOME PAGE
class UserMixin:
    def get_user(self, username_slug):
        try:
            return User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            raise Http404("User not found")

class CreateHomePageDetailView(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        homepage_detail = Homepage.objects.filter(user=user)
        serializer = HomePageSerializer(homepage_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListHomepageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = HomePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateHomePageDetailView(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def patch(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = Homepage.objects.get(id=pk, user=user)
        serializer = HomePageSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
# BLOG PAGE
class ListUserBlogView(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        blogs = Blog.objects.filter(user=user).order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUserBlogView(APIView, UserMixin):
    def get(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        blogs = get_object_or_404(Blog, id=pk , user=user)
        serializer = BlogSerializer(blogs)
        return Response(serializer.data, status=status.HTTP_200_OK)

# DOCUMENT PAGE
class ListDocumentPageDetailView(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        document_detail = DocumentPageDetail.objects.filter(user=user)
        serializer = DocumentPageDetailSerializer(document_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateDocumentPageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = DocumentPageDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateDocumentPageDetailView(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def patch(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = DocumentPageDetail.objects.get(pk=pk, user=user)
        serializer = DocumentPageDetailSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ListDocumentView(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        # Retrieve the 'name' query parameter
        name = request.query_params.get('name', None)
        # Filter documents by user and optionally by name
        if name:
            documents = Documents.objects.filter(user=user, name__icontains=name)
        else:
            documents = Documents.objects.filter(user=user)
        
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteDocumentView(APIView, UserMixin):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        document = Documents.objects.get(id=pk, user=user)
        document.delete()
        return Response("Document Delete Successfully.", status=status.HTTP_201_CREATED)
    
# CONTACT PAGE
class ContactPageView(APIView, UserMixin):
    def post(self, request, username_slug):
        user = self.get_user(username_slug)
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
    
class ListContactPerson(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        contact_persons = ContactPerson.objects.filter(user=user)
        serializer = ContactPersonSerializer(contact_persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateContactPerson(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, username_slug):
        serializer = ContactPersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateContactPerson(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def patch(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = get_object_or_404(ContactPerson, user=user, id=pk)
        serializer = ContactPersonSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteContactPerson(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def delete(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = get_object_or_404(ContactPerson, user=user, id=pk)
        instance.delete()
        return Response({"message": "Contact person deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# FEEDBACK Page, FORM AND LINK
class ListFormLinks(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        form_links = FormLinks.objects.filter(user=user)
        serializer = FormLinksSerializer(form_links, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateFormLinks(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, username_slug):
        serializer = FormLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateFormLinks(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def patch(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = get_object_or_404(FormLinks, user=user, id=pk)
        serializer = FormLinksSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteFormLinks(APIView, UserMixin):
    permission_classes = [IsAuthenticated]
    def delete(self, request, username_slug, pk):
        user = self.get_user(username_slug)
        instance = get_object_or_404(FormLinks, user=user, id=pk)
        instance.delete()
        return Response({"message": "Form link deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class MiniWebsiteOwnerDetails(APIView, UserMixin):
    def get(self, request, username_slug):
        user = self.get_user(username_slug)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)