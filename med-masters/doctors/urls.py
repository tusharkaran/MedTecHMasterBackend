from django.urls import path 
from .views import DoctorRegistration , DoctorLogin, DoctorAllResources, DoctorResource , TimeSlotsView , GetAvailTimeSlot

urlpatterns = [  
     path('', DoctorAllResources.as_view(), name='patient-list'),
     path('DoctorRegisteration', DoctorRegistration.as_view(), name='DoctorRegisteration'),   
     path('DoctorLogin', DoctorLogin.as_view(), name='DoctorLogin'),
     path('<str:user_name>', DoctorResource.as_view()),  # GET, PUT, DELETE  
     path('timeslots/<str:username>/', TimeSlotsView.as_view(), name='timeslots'),
     path('doctor/<str:doctor_username>/available-timeslots/', GetAvailTimeSlot.as_view(), name='available_timeslots'),      
]