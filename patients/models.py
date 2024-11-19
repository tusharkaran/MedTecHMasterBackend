import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Patient(models.Model):
    # Fields for the Patient model
    user_name = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    DOB = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=255)
    room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving if it is not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(Patient, self).save(*args, **kwargs)

    @classmethod
    def create_patient(cls, user_name, name, contact_number, email, role, DOB, gender, address, password):
        """
        Class method to create a new patient instance and save it to the database.
        """
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
    def get_patient_by_username(cls, username):
        """
        Fetch a patient instance based on the given username.
        """
        try:
            return cls.objects.get(user_name=username)
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_patient(cls, username, **kwargs):
        """
        Update a patient's information based on the provided keyword arguments.
        """
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
    def get_all_patients(cls):
        """
        Retrieve all patient instances from the database.
        """
        return list(cls.objects.all())

    @classmethod
    def get_room_id_by_username(cls, username):
        """
        Fetch the room_id based on the given username.
        """
        try:
            patient = cls.objects.get(user_name=username)
            return patient.room_id
        except cls.DoesNotExist:
            return None



class RecordedData(models.Model):
    record_id = models.CharField(max_length=100, unique=True)
    patient_username = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    blood_pressure = models.CharField(max_length=20)
    heart_rate = models.IntegerField()
    o2 = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Record {self.record_id} for {self.patient_username}"

    @classmethod
    def create_record(cls, record_id, patient_username, timestamp, blood_pressure, heart_rate, o2, temperature):
        record = cls(
            record_id=record_id,
            patient_username=patient_username,
            timestamp=timestamp,
            blood_pressure=blood_pressure,
            heart_rate=heart_rate,
            o2=o2,
            temperature=temperature
        )
        record.save()
        return record

    @classmethod
    def get_record_by_id(cls, record_id):
        try:
            return cls.objects.get(record_id=record_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_records(cls):
        return cls.objects.all()

    @classmethod
    def get_records_by_patient_username(cls, patient_username):
        return cls.objects.filter(patient_username=patient_username)

    @classmethod
    def get_latest_record(cls, patient_username):
        return cls.objects.filter(patient_username=patient_username).order_by('-timestamp').first()