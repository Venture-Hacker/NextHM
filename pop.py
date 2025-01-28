import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NextHM.settings')  # Replace 'your_project_name' with your actual project name
django.setup()

from property.models import Feature

def populate_features():
    features = [
        'Swimming Pool',
        'Gym',
        'Garden',
        'Parking',
        'Security System',
        'Wi-Fi Connectivity',
        'Power Backup',
        'Playground',
        'Lift',
        'Clubhouse',
        'Sports Facility'
    ]

    for feature in features:
        obj, created = Feature.objects.get_or_create(name=feature)
        if created:
            print(f"Feature '{feature}' added successfully.")
        else:
            print(f"Feature '{feature}' already exists.")

if __name__ == "__main__":
    populate_features()
