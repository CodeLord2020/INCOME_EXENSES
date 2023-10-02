from rest_framework import serializers
from .models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str, force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 8,
                                      write_only = True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
       
    
        if not username.isalnum():
            raise serializers.ValidationError('Username should contain only alphanumeric characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class SuperuserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 8, write_only = True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
       
    
        if not username.isalnum():
            raise serializers.ValidationError('Username should contain only alphanumeric characters')
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length =255)

    class Meta:
        model = User
        fields = ['tokens']

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=225)
    password =serializers.CharField(max_length = 68, write_only = True)
    tokens = serializers.CharField(max_length = 68, read_only = True)
    username =serializers.CharField(max_length = 68, read_only = True)
                                    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']

    def validate(self, attrs):
        email =attrs.get('email', '')
        password =attrs.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email not verified')

        return {
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens,
                   }
        return super().validate(attrs)

         
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
class PasswordResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 5)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 60, min_length = 6, write_only = True)
    password2 = serializers.CharField(max_length = 60, min_length = 6, write_only = True)
    token = serializers.CharField( min_length = 6, write_only = True)
    uidb64 = serializers.CharField(max_length = 60, min_length = 1, write_only = True)
    
    class Meta:
        fields = ['password','password2', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            if password == password2:
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id = id)

                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid', 401)
                user.set_password(password)
                user.save()
            else:
                raise AuthenticationFailed('Passwords do not match', 401)


        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
    
        return super().validate(attrs)