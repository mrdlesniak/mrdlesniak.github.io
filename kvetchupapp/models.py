from django.db import models

from django.utils import timezone
from datetime import datetime

from users.models import User



class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    phone_number = models.CharField(max_length=200, default="xxx-xxx-xxxx")
    customer_support_page = models.URLField(max_length=200, default="", blank=True)
    email = models.EmailField(max_length=254, default="", blank=True)
    #each site can have many reviews from many users. 
    #users can have many reviews to many sites.
    #reviews can have only one user and only one site. 

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Name: {self.name} | Id: {self.id}"

class Review(models.Model):
    review = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="reviews")
    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, blank=True, related_name="reviews") 
    review_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ['-review_date']

    def __str__(self):
        return self.review