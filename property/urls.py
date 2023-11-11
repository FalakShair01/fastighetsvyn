from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView

urlpatterns = [
    path('property/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
]