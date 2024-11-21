from rest_framework import serializers
from .models import Patient, RecordedData

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class RecordedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedData
        fields = '__all__'

