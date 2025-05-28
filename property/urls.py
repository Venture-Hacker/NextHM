from django.urls import path

from . import views

app_name = 'property'

urlpatterns = [
    path('list', views.agent_property_list, name='agent_property_list'),
    path('add', views.add_property, name='add_property'),
    #chat

]