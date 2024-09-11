from django.contrib.auth import get_user_model

from rest_framework import (status, viewsets, permissions)
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView

from authapp.serializers import (
    AdminRegistrationSerializer, UserSerializer, AdminLoginSerializer
)
from .permission import IsLibraryAdminUser


User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsLibraryAdminUser]
    
    @action(detail=False, methods=['post'], url_path='admin-signup', 
            permission_classes = [permissions.AllowAny],
            serializer_class=AdminRegistrationSerializer,)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='login',
            permission_classes = [permissions.AllowAny],
            serializer_class = AdminLoginSerializer)
    def login(self, request):
        view = TokenObtainPairView.as_view(serializer_class=AdminLoginSerializer)
        return view(request._request)
    
    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], url_path='update-me')
    def update_me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = self.perform_update(serializer)
        return Response(self.serializer_class(result).data)