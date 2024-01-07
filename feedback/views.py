from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import AdminFeedback
from .serializers import AdminFeedbackSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from users.Utils import Utils
from .filters import MarkAsDoneFilter


# Create your views here.

class AdminFeedbackViewset(viewsets.ModelViewSet):
    queryset = AdminFeedback.objects.all() 
    serializer_class = AdminFeedbackSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    filterset_class = MarkAsDoneFilter

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)    