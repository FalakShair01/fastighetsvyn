from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
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

    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete()
        instance.delete()
        return Response({"Msg": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserDevelopmentServicesView(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = UserDevelopmentServicesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevelopmentServices.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

