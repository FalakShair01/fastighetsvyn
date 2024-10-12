from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DevelopmentViewset,
    UserDevelopmentServicesViewset,
    MaintenanceViewset,
    OrderMaintenanceViewset,
    AdminDevelopemStatusView,
    AdminMaintenanceStatusView,
    ExternalSelfServiceViewSet,
    DocumentFolderDetailView,
    CreateDocumentFolderView,
    ListDocumentFolderView,
    FileCreateAPIView, 
    FileDeleteAPIView, 
    UploadFileAPIView,
    FileRetrieveAPIView,
    ServicePropertiesView,

)

router = DefaultRouter()

(router.register("development", DevelopmentViewset, basename="development-service"),)
router.register("maintenance", MaintenanceViewset, basename="maintenance-service")
(router.register("user/development", UserDevelopmentServicesViewset),)
# router.register("user/maintenance", OrderMaintenanceViewset, basename="user-maintenance")
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
    path('service/document-folders/<int:manual_service>/', ListDocumentFolderView.as_view(), name='document-folders'),
    path('service/document-folders/', CreateDocumentFolderView.as_view(), name='document-folder-create'),
    path('service/document-folders/<int:pk>/', DocumentFolderDetailView.as_view(), name='document-folder-detail'),
    path('service/file/create/', FileCreateAPIView.as_view(), name='document-create'),
    path('service/file/list/<int:folder_id>/', FileRetrieveAPIView.as_view(), name='document-create'),
    path('service/file/delete/<int:pk>/', FileDeleteAPIView.as_view(), name='document-delete'),
    path('service/file/upload/', UploadFileAPIView.as_view(), name='document-upload'),
    path('external-services/<int:service_id>/properties/', ServicePropertiesView.as_view(), name='service-properties'),
    path("", include(router.urls)),
    ]
