from django.urls import path, include
from .views import BlogListCreateView, BlogDetailView, TenantBlogView, NewsletterViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('newsletter', NewsletterViewset)

urlpatterns = [
    path('blog/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog-notification/<uid>/<blog_id>/', TenantBlogView.as_view(), name='blog-notification'),
    path('', include(router.urls))
]