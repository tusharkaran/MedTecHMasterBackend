import uuid
from django.db import models
from patients.models import Patient  # Import Patient model from patients app
from doctors.models import Doctor  # Assuming there's a Doctor model

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments", null=True, default=None)  # Temporarily allow null values
    date = models.DateField()
    day = models.CharField(max_length=20)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    room_id = models.CharField(max_length=255, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment of {self.patient} with {self.doctor} on {self.date} at {self.time}"

    @classmethod
    def create_appointment(cls, username, date, doctor_username, day, time, description):
        from patients.models import Patient
        from doctors.models import Doctor

        try:
            patient = Patient.objects.get(username=username)
            doctor = Doctor.objects.get(username=doctor_username)
        except Patient.DoesNotExist:
            return {'message': 'Patient not found'}
        except Doctor.DoesNotExist:
            return {'message': 'Doctor not found'}

        appointment = cls.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            day=day,
            time=time,
            description=description,
            room_id=patient.room_id
        )
        return appointment

    @classmethod
    def get_all_appointments(cls):
        return cls.objects.all()

    @classmethod
    def get_appointments_by_patient_username(cls, username):
        return cls.objects.filter(patient__username=username)

    @classmethod
    def get_appointments_by_doctor_username(cls, username):
        return cls.objects.filter(doctor__username=username)

    @classmethod
    def delete_appointments(cls, appointment_ids):
        cls.objects.filter(id__in=appointment_ids).delete()

    @classmethod
    def query_appointments(cls, doctor_username):
        return cls.objects.filter(
            doctor__username=doctor_username,
            date__gte=datetime.now().date()
        )
