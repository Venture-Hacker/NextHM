from django.urls import path
from .import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('contact',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('properties/',views.all_properties_view,name='all_properties_view'),
]