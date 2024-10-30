from django.urls import path 
from . import views 
from .views import AdminLoginView

app_name = 'myapp' 
urlpatterns = [ 
    path('', views.getMedAdmin, name='index'),
    path('login/', AdminLoginView.as_view(), name='admin_login'),             
]