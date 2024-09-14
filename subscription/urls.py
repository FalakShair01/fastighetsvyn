from django.urls import path
from .views import stripe_webhook, CheckSubscriptionStatus, CreateCheckoutSessionView

urlpatterns = [
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('subscription/status/', CheckSubscriptionStatus.as_view())
]
