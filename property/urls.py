from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    # path('list', views.property_list, name='property_list'),
    path('add', views.add_property, name='add_property'),
]
