from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Homepage
from .serializers import HomePageSerializer
from users.models import User


class HomepageView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username_slug):
        try:
            user = User.objects.get(username_slug=username_slug)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        homepage_detail = Homepage.objects.filter(user=user)
        serializer = HomePageSerializer(homepage_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HomePageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, username_slug, pk):
        user = User.objects.get(username_slug=username_slug)
        instance = Homepage.objects.get(id=pk, user=user)
        serializer = HomePageSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
 