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
            caption = captions.captions_dict[filename][0]
            idx = captions.captions_dict[filename][1]
        except KeyError:
            captions.captions_dict[filename] = [None, None]
            caption = None
            idx = None
        

        picture_files.append([url, caption, idx])

    picture_files.sort(key = lambda x: x[2])

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
