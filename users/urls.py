from django.urls import path, include
from .views import UserRegisterView,VerifyEmail, ProfileView, TenantView, ChangePasswordView, SendPasswordResetEmailView, ResetPasswordView, LoginView, RemoveUserProfile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tenant', TenantView, basename='tenant-create')

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("remove-profile/", RemoveUserProfile.as_view(), name="remove-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("reset-password-email/", SendPasswordResetEmailView.as_view(), name="reset-password-email"),
    path("reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
    path('', include(router.urls)),
]
