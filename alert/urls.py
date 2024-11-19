from django.urls import path
from .views import AlertResource

urlpatterns = [
    path('alerts', AlertResource.as_view(), name='alert-list'),  # For listing and creating alerts
    path('alerts/<int:alert_id>', AlertResource.as_view(), name='alert-detail'),  # For retrieving, updating, and deleting a specific alert
]
