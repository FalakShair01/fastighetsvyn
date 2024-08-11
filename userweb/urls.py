from django.urls import path
from .views import (ListHomepageDetailView, CreateHomePageDetailView, UpdateHomePageDetailView, ListUserBlogView,
                    RetrieveUserBlogView, CreateDocumentPageDetailView , ListDocumentPageDetailView, 
                    UpdateDocumentPageDetailView, CreateDocumentView, ListDocumentView, DeleteDocumentView, 
                    ContactPageView,ListContactPerson, CreateContactPerson, UpdateContactPerson, DeleteContactPerson,
                    ListFormLinks, CreateFormLinks, UpdateFormLinks, DeleteFormLinks,)

urlpatterns = [
    path('homepage/', ListHomepageDetailView.as_view(), name='homepage-create'),
    path('homepage/<slug:username_slug>/', CreateHomePageDetailView.as_view(), name='homepage-detail'),
    path('homepage/<slug:username_slug>/<int:pk>/', UpdateHomePageDetailView.as_view(), name='update-homepage'),
    path('blog/list/<slug:username_slug>/', ListUserBlogView.as_view(), name='list-blog'),
    path('blog/retrieve/<slug:username_slug>/<int:pk>/', RetrieveUserBlogView.as_view(), name='retrieve-blog'),
    path('create-document-details/', CreateDocumentPageDetailView.as_view(), name='create-doc-setail'),
    path('document-detail/retrieve/<slug:username_slug>/', ListDocumentPageDetailView.as_view(), name='list-doc-detail'),
    path('document-detail/update/<slug:username_slug>/<pk>/', UpdateDocumentPageDetailView.as_view(), name='update-doc-detail'),
    path('create-document/', CreateDocumentView.as_view(), name='create-doc'),
    path('document/retrieve/<slug:username_slug>/', ListDocumentView.as_view(), name='list-doc'),
    path('document/delete/<slug:username_slug>/<pk>/', DeleteDocumentView.as_view(), name='del-doc'),
    path('contact-us/<slug:username_slug>/', ContactPageView.as_view(), name='contact-us'),
    path('users/<str:username_slug>/contact-persons/', ListContactPerson.as_view(), name='list-contact-person'),
    path('users/<str:username_slug>/contact-persons/create/', CreateContactPerson.as_view(), name='create-contact-person'),
    path('users/<str:username_slug>/contact-persons/<int:pk>/update/', UpdateContactPerson.as_view(), name='update-contact-person'),
    path('users/<str:username_slug>/contact-persons/<int:pk>/delete/', DeleteContactPerson.as_view(), name='delete-contact-person'),
    path('users/<str:username_slug>/form-links/', ListFormLinks.as_view(), name='list-form-links'),
    path('users/<str:username_slug>/form-links/create/', CreateFormLinks.as_view(), name='create-form-links'),
    path('users/<str:username_slug>/form-links/<int:pk>/update/', UpdateFormLinks.as_view(), name='update-form-links'),
    path('users/<str:username_slug>/form-links/<int:pk>/delete/', DeleteFormLinks.as_view(), name='delete-form-links'),
]