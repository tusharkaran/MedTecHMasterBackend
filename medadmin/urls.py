from django.urls import path 
from . import views 
from .views import AdminLoginView, AdminCreateView

app_name = 'myapp' 
urlpatterns = [ 
    path('', views.getMedAdmin, name='index'),
    path('admin-login', AdminLoginView.as_view(), name='admin_login'),
     path('api/admin/create', AdminCreateView.as_view(), name='admin_create'),
]