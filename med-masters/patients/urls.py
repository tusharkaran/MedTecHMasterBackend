from django.urls import path
from .views import PatientRegistration, PatientLogin, PatientResource, RecordView, LatestRecordView, PatientAllResources, AllRecordedDataView, SendSOS

urlpatterns = [
    path('', PatientAllResources.as_view(), name='patient-list'),
    path('register', PatientRegistration.as_view(), name='patient-register'),
    path('login', PatientLogin.as_view(), name='patient-login'),
    path('record/id/<str:record_id>/', RecordView.as_view(), name='get-record'), #get by id
    path('record/<str:username>/', RecordView.as_view(), name='create-record'), #get or post by username
    # path('record/patient/<str:patient_username>/', RecordView.as_view(), name='get-records-by-patient'),
    path('latest-record/<str:username>/', LatestRecordView.as_view(), name='latest-record'), #get latest record by username
    #path('all-record/<str:username>/', AllRecordedDataView.as_view(), name='all-record'), #all records by username
    path('<str:username>', PatientResource.as_view()),
    path('sos/<str:username>/', SendSOS.as_view(), name='send_sos'),
]
