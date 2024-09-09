from django.urls import path
from .views import StripeWebhookView, CheckSubscriptionStatus

urlpatterns = [
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('subscription/status/', CheckSubscriptionStatus.as_view())
]
