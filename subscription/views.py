from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscriptionStatusSerializer, CreateCheckoutSessionSerializer, SubscriptionSerializer
from .models import Subscription
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
import stripe
from django.utils import timezone
from datetime import timedelta


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    endpoint_secret = settings.STRIPE_TEST_WEBHOOK_SECRET
    # endpoint_secret = 'whsec_d1e093c14f703db2ee8d875ad860c329ce3605bc3b1ee0ce23b7f1cae2de8bd2'
    # sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(str(e))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Signature=> {str(e)}")
        return HttpResponse(status=400)
    
    # Handle specific events
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        handle_payment_succeeded(invoice)

    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_payment_failed(invoice)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deleted(subscription)

    elif event['type'] == 'invoice.payment_action_required':
        invoice = event['data']['object']
        handle_payment_action_required(invoice)
    
    else:
        print(f"Unhandled event type: {event['type']}")

    return JsonResponse({'status': 'success'}, status=200)

    
def handle_payment_succeeded(invoice):
    subscription_id = invoice.get('subscription')
    amount_paid = invoice.get('amount_paid') / 100  # Convert cents to dollars
    subscriptions = Subscription.objects.filter(stripe_subscription_id=subscription_id)

    for subscription in subscriptions:
        subscription.last_payment_amount = amount_paid
        subscription.status = 'active'
        subscription.end_date = timezone.now() + timedelta(days=31)  # Replace with actual billing period if needed
        subscription.retry_count = 0
        subscription.save()

        user = subscription.user
        user.subscription_status = "ACTIVE"
        user.subscription_type = subscription.plan
        user.save(update_fields=["subscription_status", "subscription_type"])
        print(f"Payment succeeded for subscription: {subscription_id}")


def handle_payment_failed(invoice):
    subscription_id = invoice.get('subscription')
    subscriptions = Subscription.objects.filter(stripe_subscription_id=subscription_id)

    for subscription in subscriptions:
        subscription.retry_count += 1
        if subscription.retry_count > subscription.max_retries:
            subscription.status = 'expired'
        else:
            subscription.status = 'past_due'
        subscription.save()

        user = subscription.user
        user.subscription_status = 'past_due' if subscription.retry_count <= subscription.max_retries else 'expired'
        user.save(update_fields=["subscription_status"])
        print(f"Payment failed for subscription: {subscription_id}")


def handle_subscription_deleted(subscription):
    subscription_id = subscription.get('id')
    subscriptions = Subscription.objects.filter(stripe_subscription_id=subscription_id)

    for subscription in subscriptions:
        subscription.status = 'expired'
        subscription.save()

        user = subscription.user
        user.subscription_status = 'expired'
        user.save(update_fields=["subscription_status"])
        print(f"Subscription deleted: {subscription_id}")


def handle_payment_action_required(invoice):
    subscription_id = invoice.get('subscription')
    subscriptions = Subscription.objects.filter(stripe_subscription_id=subscription_id)

    for subscription in subscriptions:
        subscription.status = 'pending'
        subscription.save()
        print(f"Action required for subscription: {subscription_id}")


class CreateCheckoutSessionView(APIView):    
    def post(self, request):
        serializer = CreateCheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        price_id = serializer.validated_data['price_id']
        success_url = serializer.validated_data['success_url']
        cancel_url = serializer.validated_data['cancel_url']

        current_date = timezone.now()
        user = User.objects.filter(email=email).first()
        print(user)

        trial_subscription = Subscription.objects.filter(
            user=user,
            is_trial=True,
            status='active',
            end_date__isnull=False,
            end_date__gt=current_date,
        ).first()

        if trial_subscription:
            trial_subscription.status = 'expired'
            trial_subscription.end_date = current_date
            trial_subscription.save()

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=email,
            )

            Subscription.objects.create(
                user=user,
                stripe_subscription_id=session.get('subscription'),
                stripe_customer_id=session.get('customer'),
                plan=price_id,
                status='pending',
                start_date=current_date,
                is_trial=False,
            )

            return Response({'sessionId': session.id, 'url': session.url}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListPricesView(APIView):
    def get(self, request):
        try:
            # Fetch all products from Stripe
            products = stripe.Product.list(active=True)

            product_price_data = []
            for product in products.data:
                # Fetch all prices for each product
                prices = stripe.Price.list(product=product.id)

                for price in prices.data:
                    product_price_data.append({
                        'product_name': product.name,
                        'price_id': price.id,
                        'price': price.unit_amount / 100,  # Price in actual amount (Stripe stores in cents)
                        'currency': price.currency,
                        'interval': price.recurring['interval'] if price.recurring else None,
                        'type': 'recurring' if price.recurring else 'one-time',
                    })

            return Response(product_price_data, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CheckSubscriptionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve the latest subscription for the authenticated user
            user_subscription = (
                Subscription.objects.filter(user=request.user)
                .order_by('-end_date')  # Assuming `end_date` is the expiry field
                .first()
            )
            
            if not user_subscription:
                # No active subscription found; return user details
                serializer = SubscriptionStatusSerializer(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Check if the subscription is expired
            if timezone.now() > user_subscription.end_date:
                user_subscription.status = "Expired"
                user_subscription.save(update_fields=["status"])  # Save changes to the subscription
                
                # Update user's subscription status
                request.user.subscription_status = "Expired"
                request.user.save(update_fields=["subscription_status"])

            # Serialize and return the user's subscription data
            serializer = SubscriptionStatusSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred while checking subscription status: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

