from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Doctor  # Import your Doctor model
from rest_framework.exceptions import APIException
from .serializers import DoctorSerializer

class DoctorRegistration(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data

        required_fields = [
            'user_name', 'name', 'contact_number', 'email', 'role', 'DOB', 
            'gender', 'address', 'start_year_of_practice', 'specialization', 
            'study_history', 'password', 'hospital', 'availability_hours'
        ]
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new doctor instance using the class method
            response = Doctor.create_doctor(
                user_name=data.get('user_name'),
                name=data.get('name'),
                contact_number=data.get('contact_number'),
                email=data.get('email'),
                role=data.get('role'),
                DOB=data.get('DOB'),
                gender=data.get('gender'),
                address=data.get('address'),
                start_year_of_practice=data.get('start_year_of_practice'),
                availability_hours=data.get('availability_hours', []),  # Optional field with a default empty list
                specialization=data.get('specialization'),
                study_history=data.get('study_history'),
                password=data.get('password'),
                hospital=data.get('hospital')
            )
            return Response(
                {'message': 'Doctor created successfully', 'data': {'user_name': response.user_name, 'id': response.id}}, 
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
            # Check if the user exists
            doctor = Doctor.get_doctor_by_username(data['user_name'])
            if not doctor:
                return Response(
                    {'message': 'Invalid username or password (User not found)'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check if the password matches
            if not check_password(data['password'], doctor.password):
                print(f"Password check failed: Provided - {data['password']}, Hashed - {doctor.password}")
                return Response(
                    {'message': 'Invalid username or password (Incorrect password)'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(doctor)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {'access_token': access_token, 'refresh_token': refresh_token}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error during login: {str(e)}")
            return Response(
                {'message': f'Error during login: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DoctorAllResources(APIView):
    def get(self, request, *args, **kwargs):
        try:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response({'data': serializer.data})
        except ValueError as e:
            raise APIException(detail=str(e), code=400)
        except Exception as e:
            raise APIException(detail=str(e), code=500)