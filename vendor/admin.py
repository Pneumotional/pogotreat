from django.contrib import admin
from .models import VendorApplication, VendorProfile

# Register your models here.

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'commission_rate', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('business_name', 'user__username')


@admin.register(VendorApplication)
class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'full_name', 'email', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('business_name', 'full_name', 'email')