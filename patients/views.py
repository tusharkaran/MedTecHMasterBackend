from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Patient  # Import your Patient model


class PatientRegistration(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data

        required_fields = [
            'user_name', 'name', 'contact_number', 'email', 'role', 'DOB',
            'gender', 'address', 'password'
        ]

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {'message': f'Missing required fields: {", ".join(missing_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new patient instance using the class method
            response = Patient.create_patient(
                user_name=data.get('user_name'),
                name=data.get('name'),
                contact_number=data.get('contact_number'),
                email=data.get('email'),
                role=data.get('role'),
                DOB=data.get('DOB'),
                gender=data.get('gender'),
                address=data.get('address'),
                password=data.get('password')
            )
            return Response(
                {'message': 'Patient created successfully', 'data': {'user_name': response.user_name, 'id': response.id}},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': f'Error creating patient: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientLogin(APIView):
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
            # Check if the patient exists
            patient = Patient.get_patient_by_username(data['user_name'])
            if not patient:
                return Response(
                    {'message': 'Invalid username or password (User not found)'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check if the password matches
            if not check_password(data['password'], patient.password):
                return Response(
                    {'message': 'Invalid username or password (Incorrect password)'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(patient)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {'access_token': access_token, 'refresh_token': refresh_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Log the error for debugging purposes
            return Response(
                {'message': f'Error during login: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
