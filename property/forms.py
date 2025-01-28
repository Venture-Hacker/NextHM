from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'tagline', 'phone_no', 'email', 'location',
            'starting_price', 'area_size', 'category', 'cover_photo',
            'num_beds', 'num_bathrooms', 'features', 'description'
        ]
        widgets = {
            'features': forms.CheckboxSelectMultiple(attrs={'class': 'features-checkboxes'}),  # Correct widget for checkboxes
        }
