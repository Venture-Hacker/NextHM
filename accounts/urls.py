from django.urls import path
from .import views 

app_name = 'accounts'

urlpatterns = [
    path('register',views.register_view,name='register'),
    path('login',views.login_view,name='login'),
    path('agent_dashboard',views.agent_dashboard,name='agent_dashboard'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('payments', views.payments, name='payments'),
    path('payments/<str:property_id>/', views.payments, name='payments'),
    path("payment_page/", views.payment_page, name="payment_page"),
    path('processing/<int:property_id>/', views.processing_view, name='processing'),

    path('purchased_properties/', views.purchased_properties, name='purchased_properties'),
    path('delete-property/<int:property_id>/', views.delete_property_after_payment, name='delete_property_after_payment'),
    path('agent/transactions/', views.agent_transactions, name='agent_transactions'),
    path('logout',views.logout_view,name='logout'),
    path('chat/<int:property_id>/', views.chat_view, name='chat_view'),
    path('send-message/', views.send_message, name='send_message'),
    path('agent/profile/update/', views.update_agent_profile, name='update_agent_profile'),
    path('user/profile/update/', views.update_user_profile, name='update_user_profile'),
    path('agent/check-username/', views.check_username, name='check_username'),
    path('agent/check-email/', views.check_email, name='check_email'),
    
    
    ]

