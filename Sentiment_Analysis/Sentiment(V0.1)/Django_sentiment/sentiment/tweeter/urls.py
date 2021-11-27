from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
 	path('', views.chart, name='chart'),
 	path('fetch/', views.fetch, name='fetch'),
 	path('company/', views.fetch, name='company')

 	
 ]
