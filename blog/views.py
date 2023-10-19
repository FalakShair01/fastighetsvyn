from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import BlogSerializer
from .models import Blog


# Create your views here.

class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    parser_classes = [MultiPartParser, FormParser]


    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)  
     

