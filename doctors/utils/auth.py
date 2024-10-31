# utils/auth.py

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

def verify_password(stored_password_hash, input_password):
    """
    Verify if the input password matches the stored hashed password.
    """
    try:
        # Check if the input password matches the stored hash
        if password_check(stored_password_hash, input_password):
            return True
        return False
    except Exception as e:
        return JsonResponse({'message': f"Error verifying password: {str(e)}"}, status=500)

def password_hash(password):
    """
    Hash a password for storing securely.
    """
    return make_password(password)

def password_check(stored_password_hash, password):
    """
    Verify a stored password hash against an input password.
    """
    return check_password(password, stored_password_hash)

def create_token(user):
    """
    Create an access and refresh token using Django Simple JWT.
    """
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
    except Exception as e:
        return JsonResponse({'message': f"Error creating access token: {str(e)}"}, status=500)

def authenticate_user(user, input_password):
    """
    Authenticate a user with the given password.
    """
    if not verify_password(user.password, input_password):
        return JsonResponse({'message': 'Invalid credentials'}, status=401)
    return create_token(user)

def identify_current_user(request):
    """
    Identify the current user based on the JWT token using Django's request object.
    """
    try:
        current_user = request.user
        return {'user': current_user.username}
    except Exception as e:
        return JsonResponse({'message': f"Error identifying user: {str(e)}"}, status=500)
