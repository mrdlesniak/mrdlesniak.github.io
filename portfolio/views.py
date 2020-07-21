from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index(request): 
    context = {
        "activate": "about",
    }
    return render(request, 'portfolio/index.html', context)

def projects(request):
    context = {
        "activate": "projects",
    }
    return render(request, 'portfolio/projects.html', context)

def resume(request):
    context = {
        "activate": "resume",
    }
    return render(request, 'portfolio/resume.html', context)