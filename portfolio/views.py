from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index(request): 
    context = {
        "hello": "world",
    }
    return render(request, 'portfolio/index.html', context)