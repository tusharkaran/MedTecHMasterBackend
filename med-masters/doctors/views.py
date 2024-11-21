from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Doctor, Appointment , TimeSlot  # Import your Doctor model
from rest_framework.exceptions import APIException
from .serializers import DoctorSerializer , TimeSlotSerializer
from django.views import View

from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import now

class DoctorRegistration(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data

        required_fields = [
            'user_name', 'name', 'contact_number', 'email', 'role', 'DOB', 
            'gender', 'address', 'start_year_of_practice', 'specialization', 'password', 'hospital', 'availability_hours'
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
                # study_history=data.get('study_history'),
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
        

class DoctorResource(APIView):
    # Uncomment the following line to enable authentication
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_name):
        """
        Retrieve a doctor's details by username.
        """
        try:
            doctor = Doctor.objects.get(user_name=user_name)
            serializer = DoctorSerializer(doctor)
            return Response({'data': serializer.data}, status=200)
        except Doctor.DoesNotExist:
            raise APIException(detail="Doctor not found")
        except Exception as e:
            raise APIException(detail=str(e))

    def post(self, request):
        """
        Create a new doctor.
        """
        try:
            serializer = DoctorSerializer(data=request.data)
            if serializer.is_valid():
                doctor = serializer.save()
                return Response({'message': 'Doctor created successfully', 'data': serializer.data}, status=201)
            else:
                raise APIException(detail=serializer.errors)
        except Exception as e:
            raise APIException(detail=str(e))

    def put(self, request, user_name):
        """
        Update a doctor's details by username.
        """
        try:
            doctor = Doctor.objects.get(user_name=user_name)
            serializer = DoctorSerializer(doctor, data=request.data, partial=True)  # Allows partial updates
            if serializer.is_valid():
                updated_doctor = serializer.save()
                return Response({'message': 'Doctor updated successfully', 'data': serializer.data}, status=200)
            else:
                raise APIException(detail=serializer.errors)
        except Doctor.DoesNotExist:
            raise APIException(detail="Doctor not found")
        except Exception as e:
            raise APIException(detail=str(e))

    def delete(self, request, user_name):
        """
        Delete a doctor by username.
        """
        try:
            doctor = Doctor.objects.get(user_name=user_name)
            doctor.delete()
            return Response({'message': 'Doctor deleted successfully'}, status=200)
        except Doctor.DoesNotExist:
            raise APIException(detail="Doctor not found")
        except Exception as e:
            raise APIException(detail=str(e))
        


class TimeSlotsView(APIView):
 
    @staticmethod
    def generate_slot_start_times(start_time, end_time, interval_minutes=15):
        """
        Generate time slots between start_time and end_time at given intervals.
        """
        try:
            start_datetime = datetime.strptime(start_time, '%H:%M')
            end_datetime = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            raise ValueError("Invalid time format. Expected 'HH:MM'.")
 
        interval = timedelta(minutes=interval_minutes)
        current_datetime = start_datetime
        slots = []
 
        while current_datetime < end_datetime:
            slots.append(current_datetime.strftime('%H:%M'))
            current_datetime += interval
 
        return slots
 
    def post(self, request, username):
        """
        Create new time slots for a given doctor.
        """
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Invalid data format. Expected a list.'}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            doctor_instance = Doctor.objects.get(user_name=username)  # Ensure username field matches the model
            created_slots = []
 
            for item in data:
                day_name = item.get('day_name')
                start_time = item.get('start_time')
                end_time = item.get('end_time')
 
                if not day_name or not start_time or not end_time:
                    return Response({'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
 
                # Generate time slots
                try:
                    slots = self.generate_slot_start_times(start_time, end_time)
                except ValueError as e:
                    return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
                # Prepare TimeSlot objects for bulk creation
                created_slots.extend([
                    TimeSlot(
                        start_time=slot_start_time,
                        end_time=None,
                        is_booked=False,
                        day_name=day_name,
                        parent_start_time=start_time,
                        parent_end_time=end_time,
                        doctor=doctor_instance
                    )
                    for slot_start_time in slots
                ])
 
            # Bulk create time slots
            TimeSlot.objects.bulk_create(created_slots)
            serializer = TimeSlotSerializer(created_slots, many=True)
 
            return Response({'message': 'Time slots created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error creating time slots: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def get(self, request, username):
        """
        Retrieve time slots for a doctor, optionally filtered by day_name.
        """
        day_name = request.query_params.get("day_name")
        try:
            query = {'doctor__user_name': username}
            if day_name:
                query['day_name'] = day_name
 
            slots = TimeSlot.objects.filter(**query)
            if slots.exists():
                serializer = TimeSlotSerializer(slots, many=True)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Time slots not found for this doctor'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def put(self, request, username):
        """
        Update (replace) existing time slots for a doctor.
        Deletes existing slots and creates new ones based on the provided data.
        """
        data = request.data
        if not isinstance(data, list):
            return Response({'message': 'Invalid data format. Expected a list.'}, status=status.HTTP_400_BAD_REQUEST)
 
        try:
            doctor_instance = Doctor.objects.get(user_name=username)
            TimeSlot.objects.filter(doctor=doctor_instance).delete()
 
            created_slots = []
            for item in data:
                day_name = item.get('day_name')
                start_time = item.get('start_time')
                end_time = item.get('end_time')
 
                if not day_name or not start_time or not end_time:
                    return Response({'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
 
                try:
                    slots = self.generate_slot_start_times(start_time, end_time)
                except ValueError as e:
                    return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
                created_slots.extend([
                    TimeSlot(
                        start_time=slot_start_time,
                        end_time=None,
                        is_booked=False,
                        day_name=day_name,
                        parent_start_time=start_time,
                        parent_end_time=end_time,
                        doctor=doctor_instance
                    )
                    for slot_start_time in slots
                ])
 
            TimeSlot.objects.bulk_create(created_slots)
            serializer = TimeSlotSerializer(created_slots, many=True)
            return Response({'message': 'Time slots updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error updating time slots: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def delete(self, request, username):
        """
        Delete time slots for a doctor. If 'is_all' is true, delete all time slots.
        """
        is_all = request.query_params.get("is_all", "false").lower() == "true"
        try:
            if is_all:
                TimeSlot.objects.all().delete()
                return Response({'message': 'Deleted all records'}, status=status.HTTP_200_OK)
            else:
                slots = TimeSlot.objects.filter(doctor_username=username)
                if slots.exists():
                    slots.delete()
                    return Response({'message': 'Deleted all records for username'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No records found for username'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Error deleting time slots: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class GetAvailTimeSlot(View):
    def get(self, request, doctor_username):
        day_name = request.GET.get("day_name")
        try:
            if day_name:
                slots = TimeSlot.objects.filter(doctor__user_name=doctor_username, day_name=day_name).values()
            else:
                slots = TimeSlot.objects.filter(doctor__user_name=doctor_username).values()
 
            booked_appointments = self.query_appointments(doctor_username)
 
            if booked_appointments:
                for slot in slots:
                    for appointment in booked_appointments:
                        if (slot['day_name'] == appointment['day'] and
                                slot['start_time'] == appointment['time'] and
                                slot['doctor_id'] == appointment['doctor_username']):
                            slot['is_booked'] = True
                            break
 
            return JsonResponse(list(slots), safe=False, status=200)
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
 
    @staticmethod
    def query_appointments(doctor_username):
        try:
            # Get the current date
            current_date = now().date()
 
            appointments = Appointment.objects.filter(
                doctor_username=doctor_username,
                date__gt=current_date
            ).values()
 
            return list(appointments)
 
        except Exception as e:
            print(f"An error occurred while querying appointments: {str(e)}")
            return []