from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .models import Admin
from .serializer import AdminCreateSerializer
from doctors.models import Doctor
from patients.models import Patient
 
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
 
 
class AdminCreateView(APIView):
    def post(self, request):
        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Admin created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
 
class DoctorPatientRelationView(APIView):
    def post(self, request):
        """
        Link a doctor and patient.
        """
        doctor_username = request.data.get('doctor_username')
        patient_username = request.data.get('patient_username')
 
        try:
            # Fetch the doctor and patient objects
            doctor = Doctor.objects.get(user_name=doctor_username)
            patient = Patient.objects.get(user_name=patient_username)
            
            # Add the patient to the doctor's `patients` ManyToManyField
            doctor.patients.add(patient)
            patient.doctors.add(doctor)
            
            # Save is not required for ManyToManyField
            return Response(
                {'message': 'Doctor and Patient are linked successfully'},
                status=status.HTTP_200_OK,
            )
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def delete(self, request):
        """
        Unlink a doctor and patient.
        """
        doctor_username = request.data.get('doctor_username')
        patient_username = request.data.get('patient_username')
 
        try:
            doctor = Doctor.objects.get(user_name=doctor_username)
            patient = Patient.objects.get(user_name=patient_username)
            doctor.patients.remove(patient)
            doctor.save()
            patient.doctors.remove(doctor)
            patient.save()
            return Response(
                {'message': 'Patient and Doctor are unlinked successfully'},
                status=status.HTTP_200_OK,
            )
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 