from django.shortcuts import render, redirect
from core.models import *
from django.contrib import messages
from property.models import Property

# Create your views here.

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the data to the Feedback model
        Feedback.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Redirect to the same page with a success message
        return redirect(request.path + '?success=true')

    # Check if the 'success' parameter is in the query string
    success = request.GET.get('success')
    return render(request, 'index.html', {'success': success})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the data to the Feedback model
        Feedback.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Redirect to the same page with a success message
        return redirect(request.path + '?success=true')

    # Check if the 'success' parameter is in the query string
    success = request.GET.get('success')
    return render(request, 'contact.html', {'success': success})

def about(request):
    return render(request, 'about.html')

def all_properties_view(request):
    properties = Property.objects.all()
    return render(request, 'properties.html', {'properties': properties})