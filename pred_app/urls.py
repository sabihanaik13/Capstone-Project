from django.urls import path, include

from . import views

urlpatterns = [

    path('index', views.index, name='index'),
    path('pred', views.pred, name='pred'),
    path('contact', views.contact, name='contact'),  
   ]
