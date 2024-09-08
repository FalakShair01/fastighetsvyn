from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .models import Tenant, User, Managers, ServiceProvider, DemoRequests
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .Utils import Utils
import jwt
import os
from django.conf import settings
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    TenantSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    ResetPasswordSerializer,
    LoginSerializer,
    ManagerSerializer,
    ServiceProviderSerializer,
    DemoRequestSerializer,
    ContactUsSerializer,
)
from .token_utils import get_tokens_for_user
from .permissions import IsAdminOrSelf
from django.shortcuts import get_object_or_404


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """This is Used by Super admin to admin users"""
        # Generate a random password for the user
        generated_password = User.objects.make_random_password()

        # Set the generated password in the request data
        request.data["password"] = generated_password

        # # add this true because user is added by admin
        # request.data["is_active"] = True
        # request.data["is_verified"] = True

        # Use the serializer to create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email_body = f"""
                    <p>Välkommen till Fastighetsvyn!</p>
                    <p>Hej {request.data['username']}, ditt konto har skapats. Här är dina inloggningsuppgifter:</p>
                    <ul>
                        <li><strong>Email:</strong> {request.data['email']}</li>
                        <li><strong>Lösenord:</strong> {generated_password}</li>
                    </ul>
                    <p>Webbplats: <a href="{settings.FRONTEND_DOMAIN}">{settings.FRONTEND_DOMAIN}</a></p>
                """

            data = {
                "subject": "Konto Registrering",
                "body": email_body,
                "to": request.data["email"],
            }
            Utils.send_email(data=data)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            return Response(
                {
                    "Message": "Registration Fail Please try again later",
                    "Error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserRegisterView(APIView):
    def post(self, request):
        email = request.data.get("email").lower()
        if User.objects.filter(email=email).exists():
            return Response(
                {"Message": "User with email already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain

        relativeUrl = reverse("email-verify")
        absUrl = "http://" + current_site + relativeUrl + "?token=" + str(token)

        try:
            email_body = f"""
                <html>
                    <body>
                        <h2>Välkommen till vår tjänst!</h2>
                        <p>Ditt konto har skapats framgångsrikt.</p>
                        <p>Klicka på länken nedan för att verifiera ditt konto:</p>
                        <p><a href="{absUrl}">Verifiera ditt konto</a></p>
                        <p>Om du inte registrerade dig på vår webbplats, vänligen ignorera detta meddelande.</p>
                    </body>
                </html>
            """

            data = {
                "body": email_body,
                "subject": "Account Verification",
                "to": user.email,
            }
            print(data)

            Utils.send_email(data)
            return Response(
                {"Message": "Please check you Email for verification."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            user.delete()
            return Response(
                {
                    "Message": "Registration Fail Please try again later",
                    "Error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            # return render(request, 'emails/verification_success.html')
            return Response(
                {"Message": "Email Successfully activated"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    def post(self, request):
        user_type = request.query_params.get("user")

        if user_type == "manager":
            email = request.data["email"]
            password = request.data["password"]
            manager = get_object_or_404(Managers, email=email, password=password)
            if not manager.is_active:
                return Response(
                    {"Message": "User is not active. Please Contact the Support team."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            user = manager.owner
            user_data = {
                "id": manager.id,
                "email": manager.email,
                "username": manager.username,
                "phone": manager.phone,
                "password": manager.password,
                "role": manager.role,
                "is_active": manager.is_active,
                # 'subscription_type': manager.subscription_type,
                # 'allow_access_account': manager.allow_access_account,
                # Add any other fields you want to include
            }
        else:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get("email").lower()
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            user_data = UserSerializer(user).data

        if user is not None:
            if user.is_active:
                token = get_tokens_for_user(user)
                if user_type == "manager":
                    return Response(
                        {
                            "user": user_data,
                            "token": token,
                            "Message": "Login Successful",
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "user": user_data,
                            "token": token,
                            "Message": "Login Successful",
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"Message": "User is not active. Please Contact the Support team."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"Message": "Email and Password are not valid"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AdminAccessUserAccountView(APIView):
    permission_classes = [IsAdminOrSelf]

    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"Message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"Message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)
        user_data = serializer.data

        if user.is_active:
            token = get_tokens_for_user(user)
            return Response(
                {"user": user_data, "token": token, "Message": "Login Successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Message": "User is not active. Please contact the Support team."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return self.request.user


class RemoveUserProfile(APIView):
    def patch(self, request):
        instance = request.user
        serializer = ProfileSerializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        try:
            profile_path = instance.profile.path
            if profile_path and os.path.exists(profile_path):
                os.remove(profile_path)
                instance.profile = (
                    ""  # Clear the profile field after successful removal
                )
                serializer.save()
            else:
                return Response(
                    {"error": "Profile path does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"Message": "Password Has been Changed"}, status=status.HTTP_200_OK
        )


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"Message": "Password Reset Email Send Successfully"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"Message": "Password Has been Reset Successfully"},
            status=status.HTTP_200_OK,
        )


class TenantView(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Tenant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        tenant_instance = serializer.save(user=self.request.user)
        feedback_link = self.get_feedback_link(tenant_instance)
        email_body = f"""
            <p>Välkommen till Fastighetsvn!</p>
            <p>Hej {tenant_instance.name},</p>
            <p>Du har blivit tillagd av {self.request.user.username}. Nedan finns länken för återkoppling. Vänligen spara den här länken. Använd den för eventuella framtida kommentarer eller frågor, men dela den inte med någon annan.</p>
            <p>Återkoppling: <a href="{feedback_link}">Klicka här</a></p>
        """
        data = {
            "body": email_body,
            "subject": "Ditt konto har skapats - Återkopplingslänk",
            "to": tenant_instance.email,
        }
        Utils.send_email(data)
        return tenant_instance

    def get_feedback_link(self, tenant_instance):
        # Assuming the feedback URL is in a different app named 'feedback'
        feedback_url = (
            settings.FRONTEND_DOMAIN
            + f"/tenant-feedback/{self.request.user.id}/{tenant_instance.id}/"
        )
        return feedback_url


class RemoveTenantProfile(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        tenant = get_object_or_404(Tenant, user=request.user, id=pk)

        try:
            profile_path = tenant.profile.path
            if profile_path and os.path.exists(profile_path):
                os.remove(profile_path)
                tenant.profile = (
                    None  # Clear the profile field after successful removal
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = {"profile": None}
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
        serializer.validated_data["owner"] = self.request.user
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
                <p>Website: <a href="{settings.FRONTEND_DOMAIN}"{settings.FRONTEND_DOMAIN}</a></p>
            """
        data = {
            "subject": "Du läggs till som chef",
            "body": email_body,
            "to": instance.email,
        }
        Utils.send_email(data)

        # Return the result of the parent perform_create method
        return super().perform_create(serializer)


class ServerProviderViewset(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [IsAuthenticated]


class DemoRequestView(viewsets.ModelViewSet):
    queryset = DemoRequests.objects.all()
    serializer_class = DemoRequestSerializer


class SendContactUs(APIView):
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            sender_name = serializer.validated_data["name"]
            sender_phone = serializer.validated_data["phone"]
            sender_email = serializer.validated_data["email"]
            sender_message = serializer.validated_data["message"]
            admins_emails = User.objects.filter(role="ADMIN").values_list(
                "email", flat=True
            )

            subject = "Ny Kontakta oss-förfrågan"
            body = f"""
                <html>
                    <body>
                        <p>Hej Admin,</p>
                        <p>En ny förfrågan har skickats in med följande uppgifter:</p>
                        <p><strong>Namn:</strong> {sender_name}</p>      
                        <p><strong>Telefon:</strong> {sender_phone}</p>
                        <p><strong>E-post:</strong> {sender_email}</p>
                        <p><strong>Meddelande:</strong><br>{sender_message}</p>
                        <p>Vänligen granska och svara enligt behov.</p>
                    </body>
                </html>
            """
            data = {"subject": subject, "body": body, "to": list(admins_emails)}
            Utils.send_email(data)
            return Response(
                {"message": "Form submitted successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ContactUsViewset(viewsets.ModelViewSet):
#     queryset = ContactUs.objects.all()
#     serializer_class = ContactUsSerializer
#     permission_classes = [IsAuthenticated]
