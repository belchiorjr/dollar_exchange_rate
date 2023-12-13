from django.shortcuts import render
from django.http import HttpResponse
from app.sync import SyncData

# Create your views here.
def home(request):
     # SyncData()
     return render(request, 'home.html')

def search(request):
     # return render(request, 'search.html')
     return render(request, 'error.html')