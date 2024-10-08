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
    DocumentFolderViewset,
    DocumentCreateAPIView, 
    DocumentDeleteAPIView, 
    UploadDocumentAPIView

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
router.register(r'service/document-folders', DocumentFolderViewset, basename='document-folder')

urlpatterns = [
    path('service/documents/create/', DocumentCreateAPIView.as_view(), name='document-create'),
    path('service/documents/delete/<int:pk>/', DocumentDeleteAPIView.as_view(), name='document-delete'),
    path('service/documents/upload/', UploadDocumentAPIView.as_view(), name='document-upload'),
    path("", include(router.urls)),
    ]
