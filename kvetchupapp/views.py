from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from . import models
import json
import random
import string

# Create your views here.
def index(request):
    sites = models.Site.objects.order_by('name')
    message = request.GET.get('message', False)
    context = {
        "sites": sites,
        "message": message,
    }
    return render(request, 'kvetchupapp/index.html', context)  

def getSite(request): 
    siteId = request.GET.get("siteId", "error")
    if siteId == "error":
        return JsonResponse({"site": "NO SITE FOUND"})
    site = models.Site.objects.get(id=siteId)
    queryset_reviews = list(site.reviews.values()) #returns a valuequeryset. list() makes it a list of dictionaries of the reviews.
    
    for i in range(len(queryset_reviews)):
        review = queryset_reviews[i]
        review["user_id"] = str(models.User.objects.get(id=review["user_id"])) #replaces user_id with the actual user
        review["user"] = review.pop("user_id")
        #stores username 

        review['review_date'] = review['review_date'].strftime("%m/%d/%Y, %H:%M:%S")

    data = {
        "name": site.name,
        "url": site.url,
        "email": site.email,
        "phone_number": site.phone_number,
        "reviews":  queryset_reviews,
        }

    return JsonResponse({"site":data})

def formatted_phone(phone_number):
    formatted_num = ""
    for i in range(len(phone_number)):
        formatted_num += phone_number[i]
        if i == 2 or i == 5:
            formatted_num += "-"
    return formatted_num

def ratings(request):
    sites = models.Site.objects.order_by('name')
    message = request.GET.get('message', False)
    context = {
        "sites": sites,
        "message": message,
    }
    for site in sites:
        print(site.reviews)
        break
    return render(request, 'kvetchupapp/ratings.html', context) 

@login_required
def login(request):
    sites = models.Site.objects.order_by('name')
    context = {
        "sites": sites,
    }
    return render(request, 'kvetchupapp/index.html', context) 

#this method will be in charge of sending the confirmation email to verify accounts. 
def send(request):
    # send_mail(, 'mrdlesniak@gmail.com', ['mrdlesniak@gmail.com'], fail_silently=False)
    return HttpResponseRedirect(reverse('kvetchupapp:index'))

@login_required
def new_review(request):
    review_text = request.POST['review_text']
    user = request.user
    site_id = request.POST['siteId']
    site = models.Site.objects.get(id=site_id)
    review = models.Review(review=review_text, user=user, site=site )
    review.save()
    
    return HttpResponseRedirect(reverse('kvetchupapp:ratings') + '?message=True')

@login_required
def profile(request):
    message = request.GET.get('message', '')
    return render(request, 'kvetchupapp/profile.html', {'message':message})

@login_required
def edit(request):
    #get user 
    #set each value of the user instance to the new values from the edit. 
    #save
    message = "True"

    context = {
        'message': message
    }
    user = request.user
    username = request.POST['user_name']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    if models.User.objects.filter(username=username).exists() and user.username != username:
        return HttpResponseRedirect(reverse('kvetchupapp:profile') + '?message=exists')
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    
    user.save()

    return HttpResponseRedirect(reverse('kvetchupapp:profile') + '?message=True') 

@login_required
def edit_review(request): 
    new_review_txt = request.POST['review']
    review_id = request.POST['review_id']
    review_obj = models.Review.objects.get(id=review_id)
    review_obj.review = new_review_txt
    review_obj.save()
    print(review_obj.review)

    return HttpResponseRedirect(reverse('kvetchupapp:profile') + '?message=True') 

@login_required
def delete_review(request):

    review_id = request.POST['review_id']
    print("review_id" + review_id + ".")
    review = models.Review.objects.get(id=review_id)
    review.delete()

    return HttpResponseRedirect(reverse('kvetchupapp:profile') + '?message=deleted')

def about(request):
    return render(request, 'kvetchupapp/about.html')