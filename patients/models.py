import uuid
from django.db import models
from django.contrib.auth.hashers import make_password

class Patient(models.Model):
    # Fields for the Patient model
    user_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    DOB = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    doctors = models.JSONField(default=list, blank=True)
    password = models.CharField(max_length=255)
    room_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.id:
            self.password = make_password(self.password)
        super(Patient, self).save(*args, **kwargs)

    @classmethod
    def create_patient(cls, user_name, name, contact_number, email, role, DOB,
                       gender, address, password):
        hashed_password = make_password(password)
        patient = cls(
            user_name=user_name,
            name=name,
            contact_number=contact_number,
            email=email,
            role=role,
            DOB=DOB,
            gender=gender,
            address=address,
            password=hashed_password,
        )
        patient.save()
        return patient

    @classmethod
    def get_all_patients(cls):
        return list(cls.objects.all())

    @classmethod
    def get_patient_by_username(cls, username):
        try:
            return cls.objects.get(user_name=username)
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_patient(cls, username, **kwargs):
        try:
            patient = cls.objects.get(user_name=username)
            for key, value in kwargs.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)
                else:
                    return {'message': f'Attribute {key} does not exist'}
            patient.save()
            return {'message': 'Patient updated successfully'}
        except cls.DoesNotExist:
            return {'message': 'Patient not found'}
        except Exception as e:
            return {'message': 'Failed to update patient', 'error': str(e)}

    @classmethod
    def get_room_id_by_username(cls, username):
        try:
            patient = cls.objects.get(user_name=username)
            return patient.room_id
        except cls.DoesNotExist:
            return None
