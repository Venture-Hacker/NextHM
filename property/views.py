from django.shortcuts import render, redirect, get_object_or_404
from .models import Property
from .forms import PropertyForm
from django.contrib import messages

# Create your views here.

def agent_property_list(request):
    if request.method == 'POST' and 'delete' in request.GET:
        property_id = request.GET.get('delete')
        property = get_object_or_404(Property, id=property_id, agent=request.user)
        property.delete()
        messages.success(request, "Property deleted successfully!")
        return redirect('property:agent_property_list')

    properties = Property.objects.filter(agent=request.user)
    return render(request, 'agent_property_list.html', {'properties': properties})

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

