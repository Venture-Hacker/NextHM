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

    title = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default=SALE)
    cover_photo = models.ImageField(upload_to='property_photos/')
    num_beds = models.IntegerField()
    num_bathrooms = models.IntegerField()
    features = models.ManyToManyField('Feature', related_name='properties')
    description = models.TextField()
    agent = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to the agent

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
