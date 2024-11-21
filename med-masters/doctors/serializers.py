from rest_framework import serializers
from .models import Doctor, TimeSlot
 
 
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
 
 
class TimeSlotSerializer(serializers.ModelSerializer):
 
    is_booked = serializers.BooleanField(read_only=True)
 
    class Meta:
        model = TimeSlot
        fields = '__all__'
 
    def to_representation(self, instance):
        """
        Override `to_representation` to customize the output format
        for the TimeSlot model, including the `is_booked` status
        based on appointments and timeslot data.
        """
        representation = super().to_representation(instance)
 
        if hasattr(instance, 'is_booked'):
            representation['is_booked'] = instance.is_booked
 
        return representation