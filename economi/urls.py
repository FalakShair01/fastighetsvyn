from django.urls import path
from .views import (
    ExpenseListCreateView,
    ExpenseRetrieveUpdateDestroyView,
    BalanceIllustrationView,
    YearlyExpenseView,
    ImportExpensesView,
)

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path(
        "expenses/<int:pk>/",
        ExpenseRetrieveUpdateDestroyView.as_view(),
        name="expense-detail",
    ),
    path(
        "balance-illustration/",
        BalanceIllustrationView.as_view(),
        name="expense-detail",
    ),
    path("yearly-expenses/", YearlyExpenseView.as_view(), name="yearly-expenses"),
    path("import-expenses/", ImportExpensesView.as_view(), name="import_expenses"),
]
