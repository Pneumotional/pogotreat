from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from vendor.models import VendorProfile

class SaleSubmission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    items_sold = models.IntegerField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def total_revenue(self):
        return self.items_sold * self.vendor.item_rate
    
    @property
    def commission_amount(self):
        return self.total_revenue * (self.vendor.commission_rate / Decimal('100.0'))
    
    def __str__(self):
        
        return f"{self.vendor.business_name} - {self.items_sold} items - {self.status}"


class Sale(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    items_sold = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vendor.business_name} - {self.items_sold} items - ${self.amount}"

class CommissionWithdrawal(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]
    
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.business_name} - {self.amount}"