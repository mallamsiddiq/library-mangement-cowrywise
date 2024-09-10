from django.contrib.auth import get_user_model

from rest_framework import ( status, viewsets, permissions)
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView

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
    
    @action(detail=False, methods=['get'], url_path='me')
    def my_profile(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)