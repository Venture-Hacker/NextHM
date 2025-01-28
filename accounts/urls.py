from django.urls import path
from .import views 

app_name = 'accounts'

urlpatterns = [
    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('agent_dashboard',views.agent_dashboard,name='agent_dashboard'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('logout',views.logout_view,name='logout'),

]