from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from property.models import *
from accounts.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.conf import settings
from django.urls import reverse
from django.db import IntegrityError

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user_type = request.POST['user_type']  # Get the selected user type

        if password == cpassword:
            # Check if the email or username already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
                return render(request, 'register.html')  # Return to register page
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return render(request, 'register.html')  # Return to register page
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Assign user role
                if user_type == 'agent':
                    user.is_staff = True  # Mark the user as an agent
                else:
                    user.is_staff = False  # Mark the user as a regular user

                user.save()

                # Log in the user after registration
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    # Redirect based on user type
                if user.is_staff:
                    return redirect('/accounts/agent_dashboard')  # Redirect to agent dashboard
                else:
                    return redirect('/accounts/user_dashboard')  # Redirect to regular user dashboard
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')  # Return to register page
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on user type
                if user.is_staff:
                    return redirect('/accounts/agent_dashboard')  # Redirect to agent dashboard
                else:
                    return redirect('/accounts/user_dashboard')  # Redirect to regular user dashboard
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please fill out both fields')

    return render(request, 'login.html')
from accounts.models import ChatMessage
from property.models import Property
@login_required
def agent_dashboard(request):
    user = request.user
    total_listings = Property.objects.filter(agent=user).count()
    history_count = PurchasedProperty.objects.filter(agent=user).count()
    chat_count = ChatMessage.objects.filter(property__agent=user).count()
    

    # Fetch the properties for the logged-in agent
    properties = Property.objects.filter(agent=user)
    property_ids = Property.objects.values_list('id', flat=True)
    property_ids_with_chats = ChatMessage.objects.values_list('property_id', flat=True).distinct()

    # Create a list of property IDs
    property_ids = [property.id for property in properties]
    properties_with_chats = Property.objects.filter(
    agent=user,
    id__in=ChatMessage.objects.values_list('property_id', flat=True).distinct()
)

    context = {
        'total_listings': total_listings,
        'property_ids': property_ids,  # Pass the property IDs to the template
        'property_ids': property_ids,
        'properties_with_chats': properties_with_chats,
        'property_ids_with_chats': property_ids_with_chats,
        'history_count': history_count,
        'chat_count': chat_count,

    }

    return render(request, 'agent_dashboard.html', context)

@login_required
def user_dashboard(request):
    category_filter = request.GET.get('category', 'sale')  # Default to 'sale'
    location_filter = request.GET.get('location', '')  # Default to empty string (no location filter)
    search_query = request.GET.get('search', '')  # Default to empty string (no search filter)

    # Start with all properties for the selected category
    proplist = Property.objects.filter(category=category_filter)

    # Apply location filter if provided
    if location_filter:
        proplist = proplist.filter(location=location_filter)

    # Apply search filter if provided
    if search_query:
        proplist = proplist.filter(title__icontains=search_query)

    # Get distinct locations for the selected category
    distinct_locations = Property.objects.filter(category=category_filter).values('location').distinct()

    return render(request, 'user_dashboard.html', {
        'proplist': proplist,
        'selected_category': category_filter,
        'distinct_locations': distinct_locations
    })


def logout_view(request):
    auth_logout(request)
    return redirect('/accounts/login')


@login_required
def payments(request, property_id):
    property_obj = get_object_or_404(Property, property_id=property_id)
    
    context = {
        'property': property_obj,
    }
    return render(request, 'payment.html', context)

@login_required
def payment_page(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        price = request.POST.get('starting_price')
        card_number = request.POST.get('cardNumber')
        card_holder_name = request.POST.get('cardHolderName')
        exp_month = request.POST.get('expMonth')
        exp_year = request.POST.get('expYear')
        cvv = request.POST.get('cvv')

        # Simulate processing (DO NOT store card details in DB)
        try:
            property_obj = Property.objects.get(property_id=property_id)
            Payment.objects.create(
                user=request.user,
                property=property_obj,
                amount=price,
                status="SUCCESS"  # You can change this based on real processing
            )
            
            property_obj.status = 'CONFIRMED'
            property_obj.save()

            return render(request, 'payment_page.html', {'property': property_obj})
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Invalid Request", status=400)
    
@login_required
def purchased_properties(request):
    purchased_properties = PurchasedProperty.objects.filter(user=request.user).order_by('-purchase_date')  
    
    return render(request, 'purchased_properties.html', {
        'purchased_properties': purchased_properties
    })


# @login_required
def delete_property_after_payment(request, property_id):
#     # Get the property or return 404 if not found
#     property_obj = get_object_or_404(Property, id=property_id)

#     # Store the purchased property details before deletion
#     PurchasedProperty.objects.create(
#         user=request.user,
#         property_title=property_obj.title,
#         property_description=property_obj.description,
#         agent=property_obj.agent,
#         price=property_obj.starting_price,
#     )

#     # Delete the property
#     property_obj.delete()

#     # Redirect to the purchased properties page after deletion
    next_url = request.GET.get('next', 'accounts/purchased_properties')
    return redirect(next_url)

def processing_view(request, property_id):
    # Optional: delete property here if needed
    property_obj = get_object_or_404(Property, id=property_id)

    # Store the purchased property details before deletion
    PurchasedProperty.objects.create(
        user=request.user,
        property_title=property_obj.title,
        property_description=property_obj.description,
        agent=property_obj.agent,
        price=property_obj.starting_price,
    )

    # Delete the property
    property_obj.delete()

    # Redirect to the purchased properties page after deletion
    return render(request, 'processing.html', {'property_id': property_id})

def agent_transactions(request):
    sold_properties = PurchasedProperty.objects.filter(agent=request.user).order_by('-purchase_date')
    
    return render(request, 'agent_transactions.html', {'sold_properties': sold_properties})



###ag to user chat

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from property.models import Property
from django.contrib.auth.models import User

@login_required
def chat_view(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    agent = property_obj.agent

    if request.user == agent:
        user_id = request.GET.get("user_id")

        if not user_id:
            users = User.objects.filter(
                sent_messages__property=property_obj
            ).distinct()

            return render(request, "agent_chat_user_selector.html", {
                "property": property_obj,
                "users": users,
                "is_agent": True
            })

        chat_user = get_object_or_404(User, id=user_id)

        messages = ChatMessage.objects.filter(
            property=property_obj,
            sender__in=[request.user, chat_user],
            receiver__in=[request.user, chat_user]
        ).order_by("timestamp")

        return render(request, "chat.html", {
            "property": property_obj,
            "messages": messages,
            "is_agent": True,
            "agent": agent,
            "chat_user": chat_user,
            "base_template": "agentbase.html"
        })
    else:
        messages = ChatMessage.objects.filter(
            property=property_obj,
            sender__in=[request.user, agent],
            receiver__in=[request.user, agent]
        ).order_by("timestamp")

        return render(request, "chat.html", {
            "property": property_obj,
            "messages": messages,
            "is_agent": False,
            "agent": agent,
            "chat_user": agent,
            "base_template": "userbase.html"
        })

@login_required
def send_message(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        message_text = request.POST.get("message")
        receiver_id = request.POST.get("receiver_id")
        property_obj = get_object_or_404(Property, id=property_id)
        receiver = get_object_or_404(User, id=receiver_id)

        chat_message = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            property=property_obj,
            message=message_text
        )

        return JsonResponse({
            "status": "Message sent",
            "user": request.user.username,
            "message": message_text
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


from django.contrib.auth import logout

def update_agent_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Check uniqueness
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already exists.')
            return redirect('accounts:update_agent_profile')

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already exists.')
            return redirect('accounts:update_agent_profile')

        user.username = username
        user.email = email

        password_changed = False
        if password:
            user.set_password(password)
            password_changed = True

        try:
            user.save()
            if password_changed:
                logout(request)
                return render(request, 'password_changed_redirect.html')
            else:
                messages.success(request, 'Profile updated successfully!')
        except IntegrityError:
            messages.error(request, 'Error: Could not update profile due to a database issue.')

        return redirect('accounts:update_agent_profile')

    return render(request, 'agent_profile_update.html', {'user': user})

def update_user_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Check uniqueness
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already exists.')
            return redirect('accounts:update_user_profile')

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already exists.')
            return redirect('accounts:update_user_profile')

        user.username = username
        user.email = email

        password_changed = False
        if password:
            user.set_password(password)
            password_changed = True

        try:
            user.save()
            if password_changed:
                logout(request)
                return render(request, 'password_changed_redirect.html')
            else:
                messages.success(request, 'Profile updated successfully!')
        except IntegrityError:
            messages.error(request, 'Error: Could not update profile due to a database issue.')

        return redirect('accounts:update_user_profile')

    return render(request, 'user_profile_update.html', {'user': user})

def check_username(request):
    username = request.GET.get('username', '').strip()
    user_id = request.user.pk if request.user.is_authenticated else None

    exists = User.objects.filter(username=username).exclude(pk=user_id).exists()
    return JsonResponse({'exists': exists})


def check_email(request):
    email = request.GET.get('email', '').strip()
    user_id = request.user.pk if request.user.is_authenticated else None

    exists = User.objects.filter(email=email).exclude(pk=user_id).exists()
    return JsonResponse({'exists': exists})


