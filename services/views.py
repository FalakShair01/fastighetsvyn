from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import permissions
from blog.custom_permission import IsAdminUserOrReadOnly
from .models import Development, UserDevelopmentServices
from .serializers import DevelopmentSerializer, UserDevelopmentServicesSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class DevelopmentViewset(viewsets.ModelViewSet):
    queryset = Development.objects.all()
    serializer_class = DevelopmentSerializer
    permission_classes = [IsAdminUserOrReadOnly, permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class UserDevelopmentServicesView(generics.ListCreateAPIView):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = UserDevelopmentServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevelopmentServices.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

