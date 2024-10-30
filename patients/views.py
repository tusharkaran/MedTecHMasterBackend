from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def getPatients(request):
    response = HttpResponse()
    heading1 = '<p>' + 'All Patients ' + '</p>' 
    response.write(heading1)
    return response