from django.shortcuts import render
from django.http import HttpResponseRedirect
from .helpers import captions
import os


# Create your views here.
def index(request):
    picture_files = []
    for filename in os.listdir('portfolio/static/portfolio/pictures'):
        url = 'portfolio/pictures/' + filename
        
        try:
            caption = captions.captions_dict[filename]
        except KeyError:
            captions.captions_dict[filename] = None
            caption = captions.captions_dict[filename]
        

        picture_files.append([url, caption])
    

    context = {
        "activate": "about",
        "pictures": picture_files,
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