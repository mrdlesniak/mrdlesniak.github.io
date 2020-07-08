from django.db import models
import datetime

# Create your models here.
class Week(models.Model):
    week = models.CharField(max_length=200)
    year = models.CharField(max_length=200)

    #gets the first day of the week (usually sunday)
    def week_beginning(self):
        start_and_end_of_week = self.get_start_and_end_date_from_calendar_week(self.year, self.week)
        week_beginning = start_and_end_of_week[0].strftime('%m/%d/%Y')
        return week_beginning

    #gets the last day of the week (usually saturday)
    def week_end(self):
        start_and_end_of_week = self.get_start_and_end_date_from_calendar_week(self.year, self.week)
        week_end = start_and_end_of_week[1].strftime('%m/%d/%Y')
        return week_end

    #this function allows you to give a year and a week num and return the sunday and sunday of that week
    def get_start_and_end_date_from_calendar_week(self, year, calendar_week):
        sunday = datetime.datetime.strptime(f'{year}-{calendar_week}-0', "%Y-%W-%w").date()
        return sunday, sunday + datetime.timedelta(days=6.9)

    def __str__(self):
        return f"{self.week_beginning()} - {self.week_end()}"


class Date(models.Model):
    week = models.ForeignKey(Week, on_delete=models.PROTECT, related_name="dates")
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.date.strftime("%m/%d/%Y")

class Application(models.Model):
    #date, company name, location, contact method, type of work sought, results (so dumb)
    date = models.ForeignKey(Date, on_delete=models.PROTECT, related_name="applications")
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_method = models.CharField(max_length=200)
    work_type = models.CharField(max_length=200)
    results = models.CharField(max_length=200) #hired or not hired

    def __str__(self):
        return self.company_name

class Activity(models.Model):
    date = models.ForeignKey(Date, on_delete=models.PROTECT, related_name="activities")
    activity = models.CharField(max_length=200)

    def __str__(self):
        return self.activity