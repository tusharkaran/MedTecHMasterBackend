from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def getMedAdmin(request):
    response = HttpResponse()
    heading1 = '<p>' + 'All Admin ' + '</p>' 
    response.write(heading1)
    return response