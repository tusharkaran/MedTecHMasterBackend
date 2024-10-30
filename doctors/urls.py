from django.urls import path 
from . import views 
from .views import DoctorRegistration


app_name = 'myapp' 
urlpatterns = [  
     path('login/', DoctorRegistration.as_view(), name='admin_login'),            
]