from django.urls import path
from .views import (HomepageView, ListUserBlogView, RetrieveUserBlogView, DocumentPageDetailView, 
                    DocumentView, ContactPageView)

urlpatterns = [
    path('homepage/', HomepageView.as_view(), name='homepage-create'),
    path('homepage/<slug:username_slug>/', HomepageView.as_view(), name='homepage-detail'),
    path('homepage/<slug:username_slug>/<int:pk>/', HomepageView.as_view(), name='update-homepage'),
    path('blog/list/<slug:username_slug>/', ListUserBlogView.as_view(), name='list-blog'),
    path('blog/retrieve/<slug:username_slug>/<int:pk>/', RetrieveUserBlogView.as_view(), name='retrieve-blog'),
    path('create-document-details/', DocumentPageDetailView.as_view(), name='create-doc-setail'),
    path('document-detail/retrieve/<slug:username_slug>/', DocumentPageDetailView.as_view(), name='list-doc-detail'),
    path('document-detail/update/<slug:username_slug>/<pk>/', DocumentPageDetailView.as_view(), name='update-doc-detail'),
    path('create-document/', DocumentView.as_view(), name='create-doc'),
    path('document/retrieve/<slug:username_slug>/', DocumentView.as_view(), name='list-doc'),
    path('document/delete/<slug:username_slug>/<pk>/', DocumentView.as_view(), name='del-doc'),
    path('contact-us/<slug:username_slug>/', ContactPageView.as_view(), name='contact-us'),
]
