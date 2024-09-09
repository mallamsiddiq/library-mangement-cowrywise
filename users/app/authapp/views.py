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

from authapp.serializers import (
    RegistrationSerializer, UserSerializer
)

class AuthViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='register', 
            permission_classes = [permissions.AllowAny],
            serializer_class=RegistrationSerializer,)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['post'], url_path='login',
            permission_classes = [permissions.AllowAny],
            serializer_class = TokenObtainPairView.serializer_class)
    def login(self, request):
        view = TokenObtainPairView.as_view()
        return view(request._request)
    
    @action(detail=False, methods=['put'], url_path='update-me')
    def update_me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = self.perform_update(serializer)
        return Response(self.serializer_class(result).data)
    
    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)