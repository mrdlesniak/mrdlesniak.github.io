from django.urls import path
from . import views

app_name = 'jat'
urlpatterns = [
  path('jat/', views.index, name='index'),
  path('jat/new_app', views.new_app, name='new_app'),
  path('jat/new_act', views.new_act, name='new_act'),
]