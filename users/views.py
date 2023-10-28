from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .models import Tenant, User
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .Utils import Utils
import jwt
from django.conf import settings
from django.template.loader import render_to_string

from .serializers import UserSerializer, TenantSerializer, ProfileSerializer, ChangePasswordSerializer, SendPasswordResetEmailSerializer, ResetPasswordSerializer


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain

        relativeUrl = reverse('email-verify')
        absUrl = "http://" + current_site + relativeUrl + "?token=" + str(token)

        try: 
            email_body = render_to_string('emails/verify_email.html', {'username': user.username, 'absUrl': absUrl})


            data = {
                'body': email_body,
                'subject': "Verify Your Email",
                'to': user.email,
            }

            Utils.send_email(data)
            return Response({"Message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            user.delete()
            return Response({"Message": "Registration Fail Please try again later", "Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return render(request,'emails/verification_success.html')
            # return Response({'Message': 'Email Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Has been Changed"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        return Response("Password Reset Email Send Successfully", status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer()


class TenantView(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Tenant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

