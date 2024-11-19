from django.urls import path
from .views import PatientRegistration, PatientLogin, PatientResource, RecordView, LatestRecordView, PatientAllResources, AllRecordedDataView, SendSOS

urlpatterns = [
    path('', PatientAllResources.as_view(), name='patient-list'),
    path('register', PatientRegistration.as_view(), name='patient-register'),
    path('login', PatientLogin.as_view(), name='patient-login'),
    path('record/', RecordView.as_view(), name='create-record'),
    path('record/<str:record_id>/', RecordView.as_view(), name='get-record'),
    path('record/patient/<str:patient_username>/', RecordView.as_view(), name='get-records-by-patient'),
    path('latest-record/<str:username>/', LatestRecordView.as_view(), name='latest-record'),
    path('<str:username>', PatientResource.as_view()),
    path('all-record-data', AllRecordedDataView.as_view()),
    path('sos/<str:username>/', SendSOS.as_view(), name='send_sos'),
]
