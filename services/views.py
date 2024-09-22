from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import permissions
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    UserMaintenanceServices,
)
from .serializers import (
    DevelopmentSerializer,
    UserDevelopmentServicesSerializer,
    MaintainceSerializer,
    UserMaintenanceServicesSerializer,
    AdminMaintenanceStatusSerializer,
    AdminDevelopmentStatusSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from .permissions import IsAdminOrReadOnly
from .filters import UserMaintenanceFilter, UserDevelopmentFilter, DevelopmentFilter, MaintenanceFilter
# Create your views here.


class DevelopmentViewset(viewsets.ModelViewSet):
    queryset = Development.objects.all()
    serializer_class = DevelopmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = DevelopmentFilter


class UserDevelopmentServicesViewset(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = UserDevelopmentServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserDevelopmentFilter

    def get_queryset(self):
        return UserDevelopmentServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Maintenance Service
class MaintenanceViewset(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintainceSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filterset_class = MaintenanceFilter


class UserMaintenanceViewset(viewsets.ModelViewSet):
    queryset = UserMaintenanceServices.objects.all()
    serializer_class = UserMaintenanceServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = UserMaintenanceFilter

    def get_queryset(self):
        return UserMaintenanceServices.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Admin See All Pending, Active ,Completed
class AdminDevelopemStatusView(viewsets.ModelViewSet):
    queryset = UserDevelopmentServices.objects.all()
    serializer_class = AdminDevelopmentStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserDevelopmentFilter


class AdminMaintenanceStatusView(viewsets.ModelViewSet):
    queryset = UserMaintenanceServices.objects.all()
    serializer_class = AdminMaintenanceStatusSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserMaintenanceFilter
