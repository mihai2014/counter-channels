from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    #return HttpResponse("<h1>Hello!</h1>")
    return render(request, 'app/index.html', {})

