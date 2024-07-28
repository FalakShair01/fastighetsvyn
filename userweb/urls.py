from django.urls import path
from .views import HomepageView

urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='homepage-create'),
    path('homepage/<slug:username_slug>/', HomepageView.as_view(), name='homepage-detail'),
    path('homepage/<slug:username_slug>/<int:pk>/', HomepageView.as_view(), name='homepage-detail'),
]
