# microservice/middleware.py
# from requests import get as requests_get
import requests
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from library.models import User
from rest_framework import authentication, exceptions


class InternalJWTAuthMiddleware(MiddlewareMixin):
    AUTH_SERVICE_URL = getattr(settings, 'AUTH_SERVICE_URL')

    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                # Forward the Authorization header to the auth service
                response = requests.get(
                    self.AUTH_SERVICE_URL, 
                    headers={'Authorization': auth_header}
                )
                
                # Check if the auth service validated the token successfully
                if response.status_code == 200:
                    user_data = response.json()
                    request.user = self.create_user_from_data(user_data)
                
                else:
                    return JsonResponse({"detail": "Unauthorized here."}, status=401)
            
            except requests.exceptions.RequestException:
                return JsonResponse({"detail": "Auth service unavailable."}, status=503)
        
        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()

    def create_user_from_data(self, user_data):
        """Create a Django-like user object from the auth service response."""
        
        user = User(**user_data)
        return user


class JWTAuthServiceBackend(authentication.BaseAuthentication):
    AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                # Forward the Authorization header to the auth service
                response = requests.get(
                    self.AUTH_SERVICE_URL, 
                    headers={'Authorization': auth_header}
                )
                
                # Check if the auth service validated the token successfully
                if response.status_code == 200:
                    user_data = response.json()
                    user = self.create_user_from_data(user_data)
                    return user, None
                else:
                    raise exceptions.AuthenticationFailed('Unauthorized here.')
            
            except requests.exceptions.RequestException:
                raise exceptions.APIException('Auth service unavailable.', code=503)
            
            except Exception as e:
                raise exceptions.APIException(f'Auth failed {e}', code=401)

        return None

    def create_user_from_data(self, user_data):
        """Create a Django-like user object from the auth service response."""
        
        user = User(**user_data)
        return user
    
    