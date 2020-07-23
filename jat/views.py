from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Date, Application, Activity, Week
import datetime
import calendar 
from datetime import timedelta


# Create your views here.
def index(request):
    all_dates = Date.objects.order_by("-date")
    all_applications = Application.objects.order_by("company_name")
    all_activities = Activity.objects.all()
    all_weeks = Week.objects.order_by("-year", "-week")

    context = {
        "all_dates": all_dates,
        "all_applications": all_applications,
        "all_activities": all_activities,
        "all_weeks": all_weeks,
    }

    return render(request, 'jat/index.html', context)

#takes new application from form in html and saves it
#redirects back to homescreen
def new_app(request):
    new_app_date = request.POST['new_app_date']
    new_app_date = datetime.datetime.strptime(new_app_date, '%Y-%m-%d').date()

    date_exists = check_date(new_app_date)

    if date_exists:
        new_app_date = Date.objects.get(date=new_app_date)
    else:
        week = new_app_date.strftime("%V")
        year = str(new_app_date.year)
        if int(week) -2 >= 0:
            week = str(int(week) -2) #Datetime goes ahead by at least one week since Jan 1 is rarely sunday.  
        elif int(week) -2 < 0: 
            week = "51"
            year = str(int(year) - 1)
        #makes sure years aren't in a range that will break the database
        if int(year) > 9999:
            year = "9999"
        elif int(year) < 1000:
            year = "1000"
        week = save_new_week(week, year)
        new_date = Date(week=week, date=new_app_date)
        new_date.save()
        new_app_date = new_date

    new_app_co_name = request.POST['new_app_co_name']
    new_app_location = request.POST['new_app_location']
    new_app_contact_method = request.POST['new_app_contact_method']
    new_app_work_type = request.POST['new_app_work_type']
    new_app_results = request.POST['new_app_results']

    application = Application(date=new_app_date, company_name=new_app_co_name, location=new_app_location, contact_method=new_app_contact_method, work_type=new_app_work_type, results=new_app_results)
    application.save()

    return HttpResponseRedirect(reverse('jat:index'))


#takes new activity from form in html and saves it
#redirects back to homescreen
def new_act(request):
    new_act_date = request.POST['new_act_date']
    new_act_date = datetime.datetime.strptime(new_act_date, '%Y-%m-%d').date()

    date_exists = check_date(new_act_date)
    # checks if date exists. If it does, use the existing date object. 
    #If not, create one. 
    if date_exists:
        new_act_date = Date.objects.get(date=new_act_date)
    else:
        week = new_act_date.strftime("%V")
        year = str(new_act_date.year)
        if int(week) -2 >= 0:
            week = str(int(week) -2) #Datetime goes ahead by at least one week since Jan 1 is rarely sunday.  
        elif int(week) -2 < 0: 
            week = "51"
            year = str(int(year) - 1)
        #makes sure years aren't in a range that will break the database
        if int(year) > 9999:
            year = "9999"
        elif int(year) < 1000:
            year = "1000"
        week = save_new_week(week, year)
        new_date = Date(week=week, date=new_act_date)
        new_date.save()
        new_act_date = new_date
    
    new_activity = request.POST['new_activity']
    
    activity = Activity(date=new_act_date, activity=new_activity)
    activity.save()
    
    return HttpResponseRedirect(reverse('jat:index'))

#just checks if this date exists already
def check_date(new_act_date):
    all_dates = Date.objects.all()

    for date in all_dates:
        if date.date == new_act_date:
            return True
    return False

# tries to grab a week object. If it can't, it creates one.
# uses imported django exceptions. 
def save_new_week(week, year):
    try:
        week_obj = Week.objects.get(week=week, year=year)
        return week_obj
    except ObjectDoesNotExist:
        new_week = Week(week=week, year=year)
        new_week.save()
        return new_week
    except MultipleObjectsReturned:
        raise Exception("Multiple weeks. Oh no.")
    except:
        print("If try succeeds, then it escapes. If it doesn't, it should get to DoesNotExist every time. I don't know how we got here, but let's get to work! ")
        raise Exception("Bad Ending")


    