from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class VendorProfile(models.Model):
    PAYMENT_FREQUENCY_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    item_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Rate per item
    payment_frequency = models.CharField(
        max_length=10,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='MONTHLY'
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.business_name


    

    

class VendorApplication(models.Model):
    PAYMENT_FREQUENCY_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    business_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    payment_frequency = models.CharField(
        max_length=10,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='MONTHLY'
    )
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.business_name