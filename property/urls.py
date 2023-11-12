from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView, PropertyDocumentView, DeleteDocumentView

urlpatterns = [
    path('property/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('property/<int:property_id>/document/', PropertyDocumentView.as_view(), name='property-documents'),
    path('property/<int:property_id>/document-delete/<int:document_id>/', DeleteDocumentView.as_view(), name='property-documents-delete'),
]