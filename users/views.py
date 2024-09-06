from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import (
    generics, views, status, viewsets, mixins, 
    permissions
)
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from users.serializers import (
    RegistrationSerializer, PasswordResetSerializer, LogoutSerializer,
    OTPVerifySerializer, OTPGenerateSerializer, OauthTokenSerializer,
)

class AuthViewSet(viewsets.Generi):
    queryset = get_user_model().objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


    @action(detail=False, methods=['post'], url_path='login',
            serializer_class = TokenObtainPairView.serializer_class)
    def login(self, request):
        view = TokenObtainPairView.as_view()
        return view(request._request)


    @action(detail=False, methods=['post'], url_path='log-out',
            permission_classes = [permissions.IsAuthenticated], 
            serializer_class = LogoutSerializer)
    def logout(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

