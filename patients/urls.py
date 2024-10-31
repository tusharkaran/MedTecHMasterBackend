from django.urls import path
from .views import PatientRegistration, PatientLogin

urlpatterns = [
    path('register', PatientRegistration.as_view(), name='patient-register'),
    path('login', PatientLogin.as_view(), name='patient-login'),
]
