from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer
from patients.models import Patient
from doctors.models import Doctor

class AppointmentView(APIView):
    """
    Handles Appointment creation, retrieval, and deletion by patient username.
    """

    def post(self, request, username):
        """
        Create a new appointment for the given patient username.
        """
        data = request.data
        try:
            patient = get_object_or_404(Patient, user_name=username)
            doctor = get_object_or_404(Doctor, user_name=data['doctor_username'])

            # Create the appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=data['date'],
                day=data['day'],
                time=data['time'],
                description=data['description'],
                room_id=patient.room_id
            )
            return Response(
                {"message": "Appointment created successfully", "appointment_id": str(appointment.id)},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"message": f"Error creating appointment: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, username):
        """
        Get all appointments for a patient username, or all appointments if `is_all` is True.
        """
        is_all = request.query_params.get("is_all", "false").lower()
        try:
            if is_all == "true":
                appointments = Appointment.objects.all()
            else:
                patient = get_object_or_404(Patient, user_name=username)
                appointments = Appointment.objects.filter(patient=patient)

            if appointments.exists():
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No appointments found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, username):
        """
        Delete all appointments for the given patient username.
        """
        try:
            patient = get_object_or_404(Patient, user_name=username)
            appointments = Appointment.objects.filter(patient=patient)
            if appointments.exists():
                appointments.delete()
                return Response({"message": "Deleted all appointments for the patient."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No appointments found for this patient."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Error deleting appointments: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentDoctorView(APIView):
    """
    Handles Appointment retrieval and deletion by doctor username.
    """

    def get(self, request, doctor_username):
        """
        Get all appointments for a doctor username.
        """
        try:
            doctor = get_object_or_404(Doctor, user_name=doctor_username)
            appointments = Appointment.objects.filter(doctor=doctor)
            if appointments.exists():
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No appointments found for this doctor."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, doctor_username):
        """
        Delete all appointments for the given doctor username.
        """
        try:
            doctor = get_object_or_404(Doctor, username=doctor_username)
            appointments = Appointment.objects.filter(doctor=doctor)
            if appointments.exists():
                appointments.delete()
                return Response({"message": "Deleted all appointments for the doctor."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No appointments found for this doctor."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Error deleting appointments: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
