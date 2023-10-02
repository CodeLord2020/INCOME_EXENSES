from django.urls import path, reverse
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from .views import UserRegisterView, SetNewPassword, PasswordResetMail, PasswordTokenCheck,  SuperuserRegisterView, VerifyEmail, LoginAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


urlpatterns = [

    path('login/', LoginAPIView.as_view(), name = 'login'),
    path('user_register/', UserRegisterView.as_view(), name = 'user_register'),
    path('superuser_register/', SuperuserRegisterView.as_view(), name = 'superuser_register'),
    path('email-verify/', VerifyEmail.as_view(), name = 'email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('request-reset-mail/', PasswordResetMail.as_view(), name='request-reset-mail'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheck.as_view() , name = 'password-reset'),
    path('password-reset/reset/', SetNewPassword.as_view(), name = 'reset')
  
    ]

urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]