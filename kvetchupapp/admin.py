from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Site, Review, User

# Register your models here.
admin.site.register(Site)
admin.site.register(Review)
# admin.site.register(User, UserAdmin)