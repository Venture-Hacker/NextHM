from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Property(models.Model):
    SALE = 'sale'
    RENT = 'rent'
    CATEGORY_CHOICES = [
        (SALE, 'Sale'),
        (RENT, 'Rent'),
    ]
    PROPERTY_STATUS =(
    ('available','Available' ),
    ('BOOKED', 'Booked')
)
    
    property_id = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default=SALE)
    cover_photo = models.ImageField(upload_to='property_photos')
    num_beds = models.IntegerField()
    num_bathrooms = models.IntegerField()
    features = models.ManyToManyField('Feature', related_name='properties')
    description = models.TextField()
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS, default='available')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to the agent

    def save(self, *args, **kwargs):
        # Generate the property_id before saving
        if not self.property_id:
            # Check if category is Rent or Buy
            if self.category == self.RENT:
                prefix = 'RR_'
            elif self.category == self.SALE:
                prefix = 'RB_'
            else:
                prefix = ''
            
            # Generate unique ID (assuming starting from 1001)
            last_property = Property.objects.filter(category=self.category).order_by('-id').first()
            last_id = 1001 if not last_property else int(last_property.property_id.split('_')[1]) + 1
            self.property_id = f"{prefix}{last_id}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.property.title} - {self.status}"

class PurchasedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Buyer
    property_title = models.CharField(max_length=255)
    property_description = models.TextField()
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_properties")  # Add agent field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)


