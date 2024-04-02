from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import AdminFeedback, TenantsFeedback
from .serializers import AdminFeedbackSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from users.Utils import Utils
from .filters import MarkAsDoneFilter, UserFeedbackMarkAsDoneFilter
from rest_framework.views import APIView
from .serializers import UserFeedbackSerializer, GetUserFeedbackSerializer
import os


# Create your views here.

class AdminFeedbackViewset(viewsets.ModelViewSet):
    queryset = AdminFeedback.objects.all() 
    serializer_class = AdminFeedbackSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    filterset_class = MarkAsDoneFilter

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)    

class UserFeedbackView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, user, tenant):
        data = {
            'user': user,
            'tenant': tenant,
            "full_name": request.data.get('full_name'),
            "email": request.data.get('email'),
            "phone": request.data.get('phone'),
            "comment": request.data.get('comment'),
            "image": request.FILES.get('image'),  # Access file through request.FILES
        }
        serializer = UserFeedbackSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserFeedbackviewset(viewsets.ModelViewSet):
    queryset = TenantsFeedback.objects.all()
    serializer_class = GetUserFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = UserFeedbackMarkAsDoneFilter

    def get_queryset(self):
        return TenantsFeedback.objects.filter(user=self.request.user).order_by('-created_at')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image = instance.image
        if image and hasattr(image, 'path') and os.path.exists(image.path):
            os.remove(image.path)
        return super().destroy(request, *args, **kwargs)