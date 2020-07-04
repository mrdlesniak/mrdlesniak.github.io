from django.contrib import admin
from .models import Date, Application, Activity, Week

# Register your models here.
admin.site.register(Date)
admin.site.register(Application)
admin.site.register(Activity)
admin.site.register(Week)