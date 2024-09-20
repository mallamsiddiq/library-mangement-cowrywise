# auth_service/views.py
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_request(request):
    try:
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]
            
            return verify_token(token), None

        return None, "Authorization header missing or invalid."
    
    except Exception as e:
        return None, f"Invalid user. {e}"


def verify_token(token):

    # Verify the token using SimpleJWT UntypedToken
    UntypedToken(token)  # This throws an error if the token is invalid or expired

    # Optionally, decode the token using the JWTAuthentication class
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)

    # Return user details
    return {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'roles': user.roles if hasattr(user, 'roles') else None  # Example if roles exist
    }