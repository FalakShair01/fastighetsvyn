from django.urls import path
from .views import HomepageView, ListUserBlogView, RetrieveUserBlogView

urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='homepage-create'),
    path('homepage/<slug:username_slug>/', HomepageView.as_view(), name='homepage-detail'),
    path('homepage/<slug:username_slug>/<int:pk>/', HomepageView.as_view(), name='update-homepage'),
    path('blog/<slug:username_slug>/', ListUserBlogView.as_view(), name='list-blog'),
    path('blog/<slug:username_slug>/<int:pk>/', RetrieveUserBlogView.as_view(), name='retrieve-blog'),

]
