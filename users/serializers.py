from rest_framework import serializers
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import Tenant

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "phone", "address", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "phone", "address", "profile"]


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Mete:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        
        user.set_password(password)
        user.save()
        return attrs
    


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email  = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        request = self.context.get('request')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoding User id: ", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Token: ", token)
            domain = get_current_site(request).domain
            print(domain)
            url = reverse('reset-password')
            link = 'http://'+domain+url+uid+'/'+token
            print(link)


        else: 
            raise serializers.ValidationError("No User found with this Email.")
        
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("Password and Confrim Password doesn't match.")
        

        return super().validate(attrs)


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id','name', 'appartment_no', 'email', 'phone', 'profile']