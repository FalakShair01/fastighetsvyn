from django.urls import path
from .views import stripe_webhook, CheckSubscriptionStatus, CreateCheckoutSessionView, ListPricesView

urlpatterns = [
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('product/list-prices/', ListPricesView.as_view(), name='list-prices'),
    path('subscription/status/', CheckSubscriptionStatus.as_view())
]
