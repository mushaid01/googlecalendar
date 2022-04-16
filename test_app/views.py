from django.shortcuts import render
from .calendar_api import create_event

# Create your views here.
def home(request):
    return render(request, 'home.html')


def demo(request):
    results = create_event()
    context = {"results": results}
    return render(request, 'demo.html', context) 

