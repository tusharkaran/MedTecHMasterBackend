from django.urls import path
from .views import PatientRegistration, PatientLogin, PatientResource, RecordView, LatestRecordView, PatientAllResources, AllRecordedDataView, SendSOS

urlpatterns = [
    path('', PatientAllResources.as_view(), name='patient-list'),
    path('register', PatientRegistration.as_view(), name='patient-register'),
    path('login', PatientLogin.as_view(), name='patient-login'),
    path('record/id/<str:record_id>', RecordView.as_view(), name='get-record'), #get by id
    path('record/<str:username>/', RecordView.as_view(), name='create-record'), #get or post by username
    path('latest-record/<str:username>/', LatestRecordView.as_view(), name='latest-record'), #get latest record by username
    path('sos/<str:username>', SendSOS.as_view(), name='send_sos'),
    path('<str:username>', PatientResource.as_view(), name='patient-info'),
]
