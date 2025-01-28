from django.shortcuts import render, redirect
# from .models import Property
from .forms import PropertyForm
from django.contrib import messages

# Create your views here.

# def property_list(request):
#     properties = Property.objects.filter(agent=request.user)
#     return render(request, 'property_list.html', {'properties': properties})

def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.agent = request.user  # Assign the logged-in agent as the property agent
            property_instance.save()
            form.save_m2m()  # Save the many-to-many features
            messages.success(request, "Property added successfully!")
            return redirect('/accounts/agent_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PropertyForm()

    return render(request, 'add_property.html', {'form': form})
