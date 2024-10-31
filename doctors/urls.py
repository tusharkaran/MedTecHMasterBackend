from django.urls import path 
from . import views 
from .views import DoctorRegistration , DoctorLogin


app_name = 'myapp' 
urlpatterns = [  
     path('DoctorRegisteration/', DoctorRegistration.as_view(), name='DoctorRegisteration'),   
     path('DoctorLogin/', DoctorLogin.as_view(), name='DoctorLogin'),           
]