from django.urls import path 
from .views import DoctorRegistration , DoctorLogin, DoctorAllResources, DoctorResource , TimeSlotsView , GetAvailTimeSlot

urlpatterns = [  
     path('', DoctorAllResources.as_view(), name='patient-list'),
     path('DoctorRegisteration', DoctorRegistration.as_view(), name='DoctorRegisteration'),   
     path('DoctorLogin', DoctorLogin.as_view(), name='DoctorLogin'),  # GET, PUT, DELETE  
     path('timeslots/<str:username>', TimeSlotsView.as_view(), name='timeslots'),
     path('available-timeslots/<str:doctor_username>', GetAvailTimeSlot.as_view(), name='available_timeslots'),
     path('<str:user_name>', DoctorResource.as_view()),      
]
