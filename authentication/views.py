from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import UserRegisterSerializer, SuperuserRegisterSerializer,LoginSerializer,  EmailVerificationSerializer
from .serializers import PasswordResetMailSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRender



# Create your views here.



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception =True)

        return Response(serializer.data, status=status.HTTP_200_OK)

 

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    renderer_classes =[ UserRender]

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                          description = 'Description',
                                          type=openapi.TYPE_STRING )


    @swagger_auto_schema(manual_parameters =[token_param_config]) 
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        print(token)
        
        relativeLink= reverse('email-verify')
        current_site = get_current_site(request).domain
        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body= 'Hello '+ user.username+ ', use link below to verify your email\n.'+absurl
       
        data = {'domain':absurl,
                'email_body':email_body,
                'email_subject' :'Verify your email',
                'to':user.email,
                }


        Util.send_email(data)

        return Response(user_data, status = status.HTTP_201_CREATED)
    

            

class SuperuserRegisterView(generics.GenericAPIView):

    serializer_class = SuperuserRegisterSerializer
    renderer_classes =[ UserRender]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        print(token)

        return Response(user_data, status = status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='Enter Token',
                                           type= openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'},
                             status = status.HTTP_200_OK)

        except jwt.ExpiredSignatureError  as identifier:
            return Response({'error': 'Token Expired'},
                             status = status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'},
                             status = status.HTTP_400_BAD_REQUEST)


from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator        
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
class PasswordResetMail(generics.GenericAPIView):
    serializer_class = PasswordResetMailSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        email = request.data['email']

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            relativeLink= reverse('password-reset', kwargs={'uidb64':uidb64, 'token':token})
            current_site = get_current_site(request = request).domain
            absurl = 'http://' + current_site + relativeLink
            email_body= 'Hello\n, Use link below to reset your password\n.'+absurl
            print(user.id)
            print(email_body)
            data = {'domain':absurl,
                    'email_body':email_body,
                    'email_subject' :'Reset your password',
                    'to':user.email,
                    }


            Util.send_email(data)
            
        return Response({'success':' We have sent you a link to reset your password.'}, status= status.HTTP_200_OK)

from django.utils.encoding import DjangoUnicodeDecodeError, smart_str, force_str, force_bytes
class PasswordTokenCheck(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token expired, request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'user':user.username,'message':'Credentials valid', 
                              'uidb64':uidb64, 'token':token}, status= status.HTTP_200_OK)

           
        except DjangoUnicodeDecodeError as identifier:
             return Response({'error': 'Token expired, request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception =True)
        return Response({'success': True,
                          'message':'Password reset successful'},
                          status=status.HTTP_200_OK )