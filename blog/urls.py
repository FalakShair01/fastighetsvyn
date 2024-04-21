from django.urls import path, include
from .views import (BlogListCreateView, BlogDetailView, TenantBlogView, NewsletterListCreateAPIView, 
                    NewsletterRetrieveUpdateDestroyAPIView, NewsLetterSubscriberViewset)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('subscibe-newsletter', NewsLetterSubscriberViewset)

urlpatterns = [
    path('newsletter/', NewsletterListCreateAPIView.as_view(), name='newsletter-list'),
    path('newsletter/<int:pk>/', NewsletterRetrieveUpdateDestroyAPIView.as_view(), name='newsletter-detail'),
    path('blog/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog-notification/<uid>/<blog_id>/', TenantBlogView.as_view(), name='blog-notification'),
    path('', include(router.urls))
]