from django.urls import path

from . import views

urlpatterns = [

    path('index', views.index, name='index'),
    path('pred', views.pred, name='pred'),
    path('sentiment', views.sentiment, name='sentiment'),
    path('contact', views.contact, name='contact'),  
   ]
