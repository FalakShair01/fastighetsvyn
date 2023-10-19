from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import UserSerializer, TenantSerializer
from .models import Tenant, User
from rest_framework.parsers import FormParser, MultiPartParser



class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("User Created Successfully", status=status.HTTP_201_CREATED)
    

class ProfileView(APIView):

    def get(self, request):
        serialier = UserSerializer(request.user)
        return Response(serialier.data, status=status.HTTP_200_OK)



class TenantView(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

