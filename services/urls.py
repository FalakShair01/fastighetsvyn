from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DevelopmentViewset,
    UserDevelopmentServicesViewset,
    MaintenanceViewset,
    UserMaintenanceViewset,
    AdminDevelopemStatusView,
    AdminMaintenanceStatusView,
    ExternalSelfServiceViewSet,
    DocumentFolderCreateAPIView,
    DocumentFolderRetrieveUpdateDestroyAPIView

)

router = DefaultRouter()

(router.register("development", DevelopmentViewset, basename="development-service"),)
router.register("maintenance", MaintenanceViewset, basename="maintenance-service")
(router.register("user/development", UserDevelopmentServicesViewset),)
router.register("user/maintenance", UserMaintenanceViewset, basename="user-maintenance")
router.register(
    "admin/development", AdminDevelopemStatusView, basename="admin-development"
)
router.register(
    "admin/maintenance", AdminMaintenanceStatusView, basename="admin-maintenance"
)
router.register(
    "external-self-services", ExternalSelfServiceViewSet, basename="admin-maintenance"
)
urlpatterns = [
    path('service/document-folder/create/', DocumentFolderCreateAPIView.as_view(), name='document-folder-create'),
    path('service/document-folder/<int:pk>/', DocumentFolderRetrieveUpdateDestroyAPIView.as_view(), name='document-folder-detail'),
    path("", include(router.urls)),
    ]
