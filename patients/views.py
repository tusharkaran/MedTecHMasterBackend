from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Patient, RecordedData
from .serializer import PatientSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import APIException

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

class PatientResource(APIView):
    def get(self, request, username):
        patient = Patient.get_patient_by_username(username)
        if patient:
            serializer = PatientSerializer(patient)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Patient created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Error creating patient', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username):
        patient = get_object_or_404(Patient, user_name=username)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Patient updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Error updating patient', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        patient = get_object_or_404(Patient, user_name=username)
        patient.delete()
        return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    



class RecordView(APIView):
    def post(self, request):
        data = request.data
        try:
            record = RecordedData.create_record(
                record_id=data['record_id'],
                patient_username=data['patient_username'],
                timestamp=timezone.now(),
                blood_pressure=data['blood_pressure'],
                heart_rate=data['heart_rate'],
                o2=data['o2'],
                temperature=data['temperature']
            )
            return Response({'message': 'Record created successfully', 'data': record.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, record_id=None, patient_username=None):
        if record_id:
            record = RecordedData.get_record_by_id(record_id)
            if record:
                return Response({'data': record}, status=status.HTTP_200_OK)
            return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
        
        elif patient_username:
            records = RecordedData.get_records_by_patient_username(patient_username)
            return Response({'data': list(records)}, status=status.HTTP_200_OK)
        
        records = RecordedData.get_all_records()
        return Response({'data': list(records)}, status=status.HTTP_200_OK)


class LatestRecordView(APIView):
    def get(self, request, username):
        try:
            record = RecordedData.get_latest_record(username)  # Fetch latest record by username
            if record:
                return Response({'data': record}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PatientAllResources(APIView):

    def get(self, request, *args, **kwargs):
        try:
            patients = Patient.objects.all()
            serializer = PatientSerializer(patients, many=True)
            return Response({'data': serializer.data})
        except ValueError as e:
            raise APIException(detail=str(e), code=400)
        except Exception as e:
            raise APIException(detail=str(e), code=500)