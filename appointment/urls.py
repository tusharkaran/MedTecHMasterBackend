from django.urls import path
from .views import AppointmentView, AppointmentDoctorView

urlpatterns = [
    path('appointments/<str:username>/', AppointmentView.as_view(), name='appointment-by-patient'),
    path('appointments/doctor/<str:doctor_username>/', AppointmentDoctorView.as_view(), name='appointment-by-doctor'),
]
