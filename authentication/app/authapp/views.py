from django.contrib.auth import get_user_model

from rest_framework import ( status, viewsets, permissions, mixins)
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from authapp.serializers import (
    RegistrationSerializer, UserSerializer, 
    AdminRegistrationSerializer, HeaderUserSerializer
)


class AuthViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in {'retrieve', 'destroy', 'list'}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['post'], url_path='register', 
            permission_classes = [permissions.AllowAny],
            serializer_class=RegistrationSerializer,)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = self.serializer_class(user)
        return Response({'detail': 'User registered successfully'} 
                        | serializer.data, 
                        status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='login',
            permission_classes = [permissions.AllowAny],
            serializer_class = TokenObtainPairView.serializer_class)
    def login(self, request):
        view = TokenObtainPairView.as_view()
        return view(request._request)
    
    @extend_schema(
        summary="Register a new Admin user",
        description="Only emails with a @cowrywise domain are allowed to register here."
    )
    @action(detail=False, methods=['post'], url_path='admin-signup', 
            url_name='admin-signup', permission_classes = [permissions.AllowAny],
            serializer_class=AdminRegistrationSerializer,)
    def admin_signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Authenticating for protected endpoints
        user = serializer.save()
        serializer = self.serializer_class(user)
        return Response({'detail': 'User registered successfully'} 
                        | serializer.data, 
                        status=status.HTTP_201_CREATED)
    
    
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    @action(detail=False, methods=['get'], url_path='verify-header',
            serializer_class = HeaderUserSerializer,
            permission_classes = [permissions.IsAuthenticated])
    def verify_header(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
        

class ProfileViewSet(viewsets.GenericViewSet, 
                  mixins.ListModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in {'retrieve', 'destroy', 'list'}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)