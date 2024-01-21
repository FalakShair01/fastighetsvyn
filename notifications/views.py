from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AdminNotifications
from .serializers import AdminNotificationsSerializer
from .filters import IsNotificationsRead
# Create your views here.

class AdminNotificationsViewset(viewsets.ModelViewSet):
    queryset = AdminNotifications.objects.all()
    serializer_class =AdminNotificationsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = IsNotificationsRead

