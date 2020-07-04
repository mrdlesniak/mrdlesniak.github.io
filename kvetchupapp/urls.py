from django.urls import path
from . import views

app_name = 'kvetchupapp'
urlpatterns = [
    path('kvetchup/', views.index, name='index'),
    path('kvetchup/reviews/', views.ratings, name="ratings"),
    path('kvetchup/profile/', views.profile, name="profile"),
    path('kvetchup/about/', views.about, name='about'),
    path('kvetchup/getSite/', views.getSite, name='getSite'),
    path('kvetchup/login/', views.login, name='login'),
    path('kvetchup/sendmail/', views.send, name='sendmail'),
    path('kvetchup/newreview/', views.new_review, name="newreview"),
    path('kvetchup/edit/', views.edit, name="edit"),
    path('kvetchup/editReview/', views.edit_review, name="edit_review"),
    path('kvetchup/deleteReview/', views.delete_review, name="delete_review")
]