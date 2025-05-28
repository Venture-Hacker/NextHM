from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    LOCATION_CHOICES = [
        ('Alappuzha', 'Alappuzha'),
        ('Ernakulam', 'Ernakulam'),
        ('Idukki', 'Idukki'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Kozhikode', 'Kozhikode'),
        ('Malappuram', 'Malappuram'),
        ('Palakkad', 'Palakkad'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Thrissur', 'Thrissur'),
        ('Wayanad', 'Wayanad'),
    ]

    location = forms.ChoiceField(choices=LOCATION_CHOICES, label="Location", widget=forms.Select(attrs={'class': 'form-control'}))
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
