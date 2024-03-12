from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .models import Tenant, User, Managers
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .Utils import Utils
import jwt
import os
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password  # Import make_password to hash passwords
from django.contrib.auth import authenticate
from .serializers import (UserSerializer, TenantSerializer, ProfileSerializer, ChangePasswordSerializer, 
                          SendPasswordResetEmailSerializer, ResetPasswordSerializer, LoginSerializer, ManagerSerializer)
from .token_utils import get_tokens_for_user
from .permissions import IsAdminOrSelf
from django.shortcuts import get_object_or_404
import json 

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        # Generate a random password for the user
        generated_password = User.objects.make_random_password()

        # Set the generated password in the request data
        request.data['password'] = generated_password

        # Use the serializer to create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            email_body = f"""
                <p>Välkommen till Fastighetsvn!</p>
                <p>Hej {request.data['username']}, Ditt konto har skapats. Här är dina inloggningsuppgifter:</p>
                <ul>
                    <li><strong>Email:</strong> {request.data['email']}</li>
                    <li><strong>Password:</strong> {generated_password}</li>
                </ul>
                <p>Website: <a href="https://fastighetsvyn.se/">https://fastighetsvyn.se/</a></p>
            """

            data = {
                "subject": "Account Registration",
                "body": email_body,
                "to": request.data['email']
            }
            Utils.send_email(data=data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({"Message": "Registration Fail Please try again later", "Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class UserRegisterView(APIView):

    def post(self, request):
        email = request.data.get('email').lower()
        if User.objects.filter(email=email).exists():
            return Response({"Message": "User with email already exist"}, status=status.HTTP_400_BAD_REQUEST)
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
            # email_body = render_to_string(
            #     'emails/verify_email.html', {'title': 'Account Verification','username': user.username, 'absUrl': absUrl, 'message': 'Thank you for registering with Fastighetsvyn. To complete your registration, please click the following link to verify your email address:', 'endingMessage':"If you did not register on Fastighetsvyn, please disregard this email.", 'btn': 'Verify Email'})

            data = {
                'body': "Your Account is created",
                'subject': "Account Verification",
                'to': user.email,
            }

            # Utils.send_email(data)
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
        user_type = request.query_params.get('user')

        if user_type == 'manager':
            email = request.data['email']
            password = request.data['password']
            manager = get_object_or_404(Managers, email=email, password=password)
            user = manager.owner
            user_data = {
                'id': manager.id,
                'email': manager.email,
                'username': manager.full_name,
                'phone': manager.phone,
                'password': manager.password,
                'role': manager.role,
                'is_active': manager.is_active
                # Add any other fields you want to include
            }
        else:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email').lower()
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            user_data = UserSerializer(user).data

        if user is not None:
            if user.is_active:
                token = get_tokens_for_user(user)
                if user_type == 'manager':
                    return Response({'user': user_data, 'token': token, "Message": "Login Successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({'user': user_data, 'token': token, "Message": "Login Successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": "User is not active. Please Contact the Support team."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Message": "Email and Password are not valid"}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            profile_path = instance.profile.path
            if profile_path and os.path.exists(profile_path):
                os.remove(profile_path)
        except Exception as e:
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
    

class RemoveTenantProfile(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        tenant = Tenant.objects.get(user=request.user, id=pk)
        try:
            profile_path = tenant.profile.path
            if profile_path and os.path.exists(profile_path):
                os.remove(profile_path)
        except Exception as e:
            
            data = {'profile':None}
            serializer = TenantSerializer(tenant, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ManagersViewset(viewsets.ModelViewSet):
    queryset = Managers.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Managers.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        # Call the parent perform_create method to save the instance
        instance = serializer.save()

        # Your custom logic to send an email
        email_body = f"""
                <p>Välkommen till Fastighetsvn!</p>
                <p>Hej {instance.full_name}, Ditt konto har skapats. Här är dina inloggningsuppgifter:</p>
                <ul>
                    <li><strong>Email:</strong> {instance.email}</li>
                    <li><strong>Password:</strong> {instance.password}</li>
                </ul>
                <p>Website: <a href="https://fastighetsvyn.se/">https://fastighetsvyn.se/</a></p>
            """
        data = {
            'subject': 'Du läggs till som chef',
            'body': email_body,
            'to': instance.email
        }
        Utils.send_email(data)

        # Return the result of the parent perform_create method
        return super().perform_create(serializer)