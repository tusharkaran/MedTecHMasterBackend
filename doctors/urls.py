from django.urls import path 
from . import views 

app_name = 'myapp' 
urlpatterns = [ 
    path('', views.getDoctors, name='index')             
]