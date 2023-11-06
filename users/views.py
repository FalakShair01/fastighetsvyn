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
from .Utils import Utils
import jwt
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from .serializers import UserSerializer, TenantSerializer, ProfileSerializer, ChangePasswordSerializer, SendPasswordResetEmailSerializer, ResetPasswordSerializer, LoginSerializer
from .token_utils import get_tokens_for_user


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
            email_body = render_to_string(
                'emails/verify_email.html', {'title': 'Account Verification','username': user.username, 'absUrl': absUrl, 'message': 'Thank you for registering with Fastighetsvyn. To complete your registration, please click the following link to verify your email address:', 'endingMessage':"If you did not register on Fastighetsvyn, please disregard this email."})

            data = {
                'body': email_body,
                'subject': "Account Verification",
                'to': user.email,
            }

            Utils.send_email(data)
            return Response({"Message": "Please check you Email for verification."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            user.delete()
            return Response({"Message": "Registration Fail Please try again later", "Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return render(request, 'emails/verification_success.html')
            # return Response({'Message': 'Email Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                if user.is_verified:
                    token = get_tokens_for_user(user)
                    return Response({'token': token,"Message":"Login Successfull"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "User is not verified"})
            else:
                return Response({"Message": "User is not active"})
        else:
            return Response({"Message":"Email and Password is not valid"})


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return self.request.user


class RemoveUserProfile(APIView):
    def patch(self, request):
        instance=request.user
        serializer = ProfileSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.profile = ""
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Has been Changed"}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Reset Email Send Successfully"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data, context={
                                             'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({"Message": "Password Has been Reset Successfully"}, status=status.HTTP_200_OK)


class TenantView(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Tenant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)