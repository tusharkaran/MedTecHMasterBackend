from django.urls import path 
from . import views 
from .views import AdminLoginView, AdminCreateView, DoctorPatientRelationView


urlpatterns = [ 
    path('', views.getMedAdmin, name='index'),
    path('admin-login', AdminLoginView.as_view(), name='admin_login'),
     path('create', AdminCreateView.as_view(), name='admin_create'),
     path('doctorpatientrelation', DoctorPatientRelationView.as_view(), name='doctor_patient_relation'),
]