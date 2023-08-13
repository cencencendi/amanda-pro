from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.


def calibration(request):
    return render(request, 'calibration.html')