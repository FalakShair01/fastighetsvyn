from django.urls import path
from .views import ExpenseListCreateView, ExpenseRetrieveUpdateDestroyView

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyView.as_view(), name='expense-detail'),
]
