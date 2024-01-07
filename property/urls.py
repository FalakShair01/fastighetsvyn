from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PropertyListCreateView, PropertyDetailView, PropertyDocumentView, DeleteDocumentView, 
                    GetPieChartView, PropertyExportAPIView, FolderViewset)

router = DefaultRouter()
router.register(r'property/(?P<property_id>\d+)/folder', FolderViewset, basename='property-folder')

urlpatterns = [
    path('property/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('property/<int:folder_id>/document/', PropertyDocumentView.as_view(), name='property-documents'),
    path('property/<int:folder_id>/document-delete/<int:document_id>/', DeleteDocumentView.as_view(), name='property-documents-delete'),
    path('property/chart/', GetPieChartView.as_view()),
    path('property/export/', PropertyExportAPIView.as_view()),

    path('', include(router.urls))
]