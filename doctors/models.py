import uuid
from django.db import models
from django.contrib.auth.hashers import make_password

class Doctor(models.Model):
    # Fields for the Doctor model
    user_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    DOB = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    start_year_of_practice = models.IntegerField()
    availability_hours = models.JSONField(default=list, blank=True)
    specialization = models.CharField(max_length=255)
    study_history = models.JSONField(default=list, blank=True)
    patients = models.JSONField(default=list, blank=True)
    password = models.CharField(max_length=255)
    hospital = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if not self.id:
            self.password = make_password(self.password)
        super(Doctor, self).save(*args, **kwargs)

    @classmethod
    def create_doctor(cls, user_name, name, contact_number, email, role, DOB, gender, address, start_year_of_practice,
                      specialization, study_history, password, hospital):
        hashed_password = make_password(password)
        doctor = cls(
            user_name=user_name,
            name=name,
            contact_number=contact_number,
            email=email,
            role=role,
            DOB=DOB,
            gender=gender,
            address=address,
            start_year_of_practice=start_year_of_practice,
            specialization=specialization,
            study_history=study_history,
            password=hashed_password,
            hospital=hospital,
        )
        doctor.save()
        return doctor

    @classmethod
    def get_all_doctors(cls):
        return list(cls.objects.all())

    @classmethod
    def get_doctor_by_username(cls, username):
        try:
            return cls.objects.get(user_name=username)
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_doctor(cls, username, **kwargs):
        try:
            doctor = cls.objects.get(user_name=username)
            for key, value in kwargs.items():
                if hasattr(doctor, key):
                    setattr(doctor, key, value)
                else:
                    return {'message': f'Attribute {key} does not exist'}
            doctor.save()
            return {'message': 'Doctor updated successfully'}
        except cls.DoesNotExist:
            return {'message': 'Doctor not found'}
        except Exception as e:
            return {'message': 'Failed to update doctor', 'error': str(e)}
