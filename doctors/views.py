from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Doctor  # Import your Doctor model
from .utils.auth import verify_password  # Import your verify_password utility

class DoctorRegistration(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data

        required_fields = [
            'user_name', 'name', 'contact_number', 'email', 'role', 'DOB', 
            'gender', 'address', 'start_year_of_practice', 'specialization', 
            'study_history', 'password', 'Hospital'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new doctor instance
            new_doctor = Doctor()
            # Call the create method and pass the data (assuming create_doctor is a method in your Doctor model)
            response = new_doctor.create_doctor(**data)
            return Response(
                {'message': 'Doctor created successfully', 'data': response}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': f'Error creating doctor: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DoctorLogin(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data
        required_fields = ['user_name', 'password']

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doctor = Doctor.get_doctor_by_username(data['user_name'])
            if doctor and verify_password(data['password'], doctor.password):
                refresh = RefreshToken.for_user(doctor)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response(
                    {'access_token': access_token, 'refresh_token': refresh_token}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Invalid username or password'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {'message': f'Error during login: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
