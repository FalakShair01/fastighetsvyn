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
    sig_header = request.headers['STRIPE_SIGNATURE']

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
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        data = {
            "status": "Active",
            "_id": payment_intent.get('id'),
            "amount": payment_intent.get('amount'),
            "amount_received": payment_intent.get('amount_received'),
            "currency": payment_intent.get('currency'),
            "customer": payment_intent.get("customer"),
            "receipt_email": payment_intent.get("receipt_email"),
            "subscription_expiry": timezone.now() + timedelta(days=31),
            "subscription_type": "Paid",
        }
        serializer = SubscriptionSerializer(data=data)  
        serializer.is_valid(raise_exception=True) 
        serializer.save()
    return HttpResponse(status=200)


# View to create a Checkout Session
class CreateCheckoutSessionView(APIView):
    def post(self, request):
        serializer = CreateCheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        price_id = serializer.validated_data['price_id']
        success_url = serializer.validated_data['success_url']
        cancel_url = serializer.validated_data['cancel_url']

        try:
            # Create a Checkout Session with the email
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',  # Change to 'payment' for one-time payments
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=email,  # Pre-fill the customer's email
            )
            return Response({'sessionId': session.id, 'url': session.url}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
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
            user_subscription = Subscription.objects.filter(user=request.user).order_by('-subscription_expiry').first()
            
            if not user_subscription:
                # Return user details with no active subscription
                serializer = SubscriptionStatusSerializer(request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Check if the subscription is expired
            if timezone.now() > user_subscription.subscription_expiry:
                user_subscription.status = "Expired"
                user_subscription.save()  # Save changes to the subscription
                
                # Update user status if required (assuming `status` is a field on the User model)
                request.user.subscription_status = "Expired"
                request.user.save()

            # Serialize and return the user's subscription data
            serializer = SubscriptionStatusSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

