from django.contrib import admin
from .models import Sale, CommissionWithdrawal, SaleSubmission
from  django.utils import timezone
from django.contrib import messages

# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'amount', 'commission_amount', 'created_at')
    list_filter = ('vendor', 'created_at')
    search_fields = ('vendor__business_name',)

@admin.register(CommissionWithdrawal)
class CommissionWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'amount', 'status', 'request_date', 'processed_date')
    list_filter = ('status', 'request_date')
    search_fields = ('vendor__business_name',)
    

@admin.register(SaleSubmission)
class SaleSubmissionAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'status', 'total_revenue', 'commission_amount', 'processed_at')
    # actions = None  # Optional: Disables bulk actions if not needed

    # def save_model(self, request, obj, form, change):
    #     # Only create Sale if the status is changed to 'Approved'
    #     if change:  # Only if the object is being updated (not created)
    #         if obj.status == 'Approved' and not obj.processed_at:  # Ensure it's not already processed
    #             # Create a new Sale record
    #             Sale.objects.create(
    #                 vendor=obj.vendor,
    #                 items_sold=obj.items_sold,
    #                 amount=obj.total_revenue,
    #                 commission_amount=obj.commission_amount
    #             )
                
    #             # Update the processed_at field
    #             obj.processed_at = timezone.now()
    #             messages.success(request, 'Sale record created automatically after approval.')

    #     super().save_model(request, obj, form, change)