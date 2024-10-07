from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DevelopmentViewset,
    UserDevelopmentServicesViewset,
    MaintenanceViewset,
    UserMaintenanceViewset,
    AdminDevelopemStatusView,
    AdminMaintenanceStatusView,
    ExternalSelfServiceView,
    ExternalSelfServiceDetailView, 
    ExternalSelfServiceDetailUpdate,
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

urlpatterns = [
    path('external-self-services/', ExternalSelfServiceView.as_view(), name='external-self-service-list'),
    path('external-self-services/<int:pk>/', ExternalSelfServiceDetailView.as_view(), name='external-self-service-detail'),
    path('external-self-services/<int:pk>/update/', ExternalSelfServiceDetailUpdate.as_view(), name='external-self-service-update'),
    path('service/document-folder/create/', DocumentFolderCreateAPIView.as_view(), name='document-folder-create'),
    path('service/document-folder/<int:pk>/', DocumentFolderRetrieveUpdateDestroyAPIView.as_view(), name='document-folder-detail'),
    path("", include(router.urls)),]
