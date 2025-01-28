from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

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

@login_required
def agent_dashboard(request):
        return render(request, 'agent_dashboard.html')

@login_required
def user_dashboard(request):
        return render(request, 'user_dashboard.html')

def logout_view(request):
    auth_logout(request)
    return redirect('/accounts/login')
