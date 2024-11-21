from django.contrib import admin
from .models import Patient, RecordedData

# Register your models here. 
admin.site.register(Patient) 
admin.site.register(RecordedData)