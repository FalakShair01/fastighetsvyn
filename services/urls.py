from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DevelopmentViewset,
    UserDevelopmentServicesViewset,
    MaintenanceViewset,
    AdminDevelopemStatusView,
    ExternalSelfServiceViewSet,
    DocumentFolderDetailView,
    CreateDocumentFolderView,
    ListDocumentFolderView,
    FileCreateAPIView, 
    FileDeleteAPIView, 
    UploadFileAPIView,
    FileRetrieveAPIView,
    ListOrderMaintenanceAPIView,
    CreateOrderMaintenanceAPIView,
    UpdateOrderMaintenanceAPIView,
    DeleteOrderMaintenanceAPIView,
    ListOrderServiceFolderView,
    CreateOrderServiceFolderView,
    UpdateOrderServiceFolderView,
    DeleteOrderServiceFolderView,
    CreateOrderServiceFileView,
    DeleteOrderServiceFileView
)

router = DefaultRouter()

(router.register("development", DevelopmentViewset, basename="development-service"),)
router.register("maintenance", MaintenanceViewset, basename="maintenance-service")
(router.register("user/development", UserDevelopmentServicesViewset),)
router.register(
    "admin/development", AdminDevelopemStatusView, basename="admin-development"
)
router.register(
    "external-self-services", ExternalSelfServiceViewSet, basename="admin-maintenance"
)

urlpatterns = [
    # --------- order maintenance service ----------
    path('service/orders/list/', ListOrderMaintenanceAPIView.as_view(), name='order-list'),
    path('service/orders/create/', CreateOrderMaintenanceAPIView.as_view(), name='order-create'),
    path('service/orders/<int:pk>/update/', UpdateOrderMaintenanceAPIView.as_view(), name='order-update'),
    path('service/orders/<int:pk>/delete/', DeleteOrderMaintenanceAPIView.as_view(), name='order-delete'),
    path('order-service/<int:order_service>/list/', ListOrderServiceFolderView.as_view(), name='list_order_service_folders'),
    path('order-service/folders/', CreateOrderServiceFolderView.as_view(), name='create_order_service_folder'),
    path('order-service/folders/<int:id>/', UpdateOrderServiceFolderView.as_view(), name='update_order_service_folder'),
    path('order-service/folders/<int:id>/delete/', DeleteOrderServiceFolderView.as_view(), name='delete_order_service_folder'),
    path('order-service/files/', CreateOrderServiceFileView.as_view(), name='create_order_service_file'),
    path('order-service/files/<int:pk>/delete/', DeleteOrderServiceFileView.as_view(), name='delete_order_service_file'),
    # --------- manuall maintenance service ----------
    path('service/document-folders/<int:manual_service>/list/', ListDocumentFolderView.as_view(), name='document-folders'),
    path('service/document-folders/', CreateDocumentFolderView.as_view(), name='document-folder-create'),
    path('service/document-folders/<int:pk>/', DocumentFolderDetailView.as_view(), name='document-folder-detail'),
    path('service/file/create/', FileCreateAPIView.as_view(), name='document-create'),
    path('service/file/list/<int:folder_id>/', FileRetrieveAPIView.as_view(), name='document-create'),
    path('service/file/delete/<int:pk>/', FileDeleteAPIView.as_view(), name='document-delete'),
    path('service/file/upload/', UploadFileAPIView.as_view(), name='document-upload'),
    path("", include(router.urls)),
    ]
