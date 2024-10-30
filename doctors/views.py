from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def getDoctors(request):
    response = HttpResponse()
    heading1 = '<p>' + 'All doctors ' + '</p>' 
    response.write(heading1)
    return response