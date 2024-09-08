from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SubscriptionStatusSerializer
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class StripeWebhookView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            print(f"event data {event}")
        except ValueError as e:
            return JsonResponse({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Handle successful checkout session here
        # if event.type == 'payment_intent.succeeded':
        #     payment_intent = event.data.object # contains a stripe.PaymentIntent
        #     print(f'PaymentIntent was successful! {payment_intent}')
        # elif event.type == 'payment_method.attached':
        #     payment_method = event.data.object # contains a stripe.PaymentMethod
        #     print('PaymentMethod was attached to a Customer!')


        return JsonResponse({'status': 'success'})
