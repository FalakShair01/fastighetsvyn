from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import AdminFeedback, UserFeedback
from .serializers import AdminFeedbackSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from users.models import User, Tenant
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

    def post(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        tenant_email = request.data.get('email')
        try:
            tenant = Tenant.objects.get(email=tenant_email)
        except Tenant.DoesNotExist:
            return Response({"error": "Your email doesn't exist in the system. Please retry with a registered email."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'user': user.id,  
            'tenant': tenant.id,  
            "property": request.data.get('property'),
            "full_name": request.data.get('full_name'),
            "email": tenant_email,
            "phone": request.data.get('phone'),
            "comment": request.data.get('comment'),
            "image": request.FILES.get('image'),  # Access file through request.FILES
        }

        serializer = UserFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserFeedbackviewset(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = GetUserFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = UserFeedbackMarkAsDoneFilter

    def get_queryset(self):
        return UserFeedback.objects.filter(user=self.request.user).order_by('-created_at')
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image = instance.image
        if image and hasattr(image, 'path') and os.path.exists(image.path):
            os.remove(image.path)
        return super().destroy(request, *args, **kwargs)