from django.urls import path
from .views import stripe_webhook, CheckSubscriptionStatus, CreateCheckoutSessionView, ListPricesView, ExtendSubscriptionView

urlpatterns = [
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('product/list-prices/', ListPricesView.as_view(), name='list-prices'),
    path('subscription/status/', CheckSubscriptionStatus.as_view()),
    path('api/extend-subscription/', ExtendSubscriptionView.as_view(), name='extend_subscription'),
]
