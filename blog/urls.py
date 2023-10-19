from django.urls import path, include
from .views import BlogView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', BlogView, basename="create-blog")


urlpatterns = [
    path('', include(router.urls))
]