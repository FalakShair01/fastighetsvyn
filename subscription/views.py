from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscriptionStatusSerializer, CreateCheckoutSessionSerializer
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'your-webhook-secret'
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Fulfill the purchase or update payment status in your database
        print('Payment succeeded:', payment_intent.id)
    
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

            return Response({'sessionId': session.id}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckSubscriptionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       serializer = SubscriptionStatusSerializer(request.user)
       return Response(serializer.data, status=status.HTTP_200_OK)
