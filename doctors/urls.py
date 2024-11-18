from django.urls import path 
from .views import DoctorRegistration , DoctorLogin, DoctorAllResources


app_name = 'myapp' 
urlpatterns = [  
     path('', DoctorAllResources.as_view(), name='patient-list'),
     path('DoctorRegisteration', DoctorRegistration.as_view(), name='DoctorRegisteration'),   
     path('DoctorLogin', DoctorLogin.as_view(), name='DoctorLogin'),        
]