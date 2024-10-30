from django.shortcuts import render
from django.http import HttpResponse 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .models import Admin

# Create your views here.
def getMedAdmin(request):
    response = HttpResponse()
    heading1 = '<p>' + 'All Admin ' + '</p>' 
    response.write(heading1)
    return response


class AdminLoginView(APIView):
    def post(self, request):
        # Retrieve and validate data from request
        user_name = request.data.get('user_name')
        password = request.data.get('password')

        if not user_name or not password:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the admin exists
        admin = get_object_or_404(Admin, user_name=user_name)

        # Verify password
        if not check_password(password, admin.password):
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(admin)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return tokens in the response
        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)
