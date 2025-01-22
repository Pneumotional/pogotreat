# views.py
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import SaleSubmission, Sale
from .forms import SaleSubmissionForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def submit_sales(request):
    if request.method == 'POST':
        form = SaleSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.vendor = request.user.vendorprofile
            submission.save()
            messages.success(request, 'Sales submission has been sent for approval.')
            return redirect('vendor_dashboard')
    else:
        form = SaleSubmissionForm()
    
    return render(request, 'submit_sales.html', {'form': form})

@login_required
@staff_member_required
def pending_sales(request):
    submissions = SaleSubmission.objects.filter(status='PENDING').order_by('-submitted_at')
    return render(request, 'admin/pending_sales.html', {'submissions': submissions})

@login_required
@staff_member_required
def process_sale_submission(request, submission_id):
    submission = get_object_or_404(SaleSubmission, id=submission_id)
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'approve':
            # Create approved sale
            Sale.objects.create(
                vendor=submission.vendor,
                items_sold=submission.items_sold,
                amount=submission.total_revenue,
                commission_amount=submission.commission_amount
            )
            
            submission.status = 'APPROVED'
            submission.processed_at = timezone.now()
            submission.save()
            
            messages.success(request, 'Sale submission approved successfully.')
        
        elif action == 'reject':
            submission.status = 'REJECTED'
            submission.processed_at = timezone.now()
            submission.save()
            
            messages.success(request, 'Sale submission rejected.')
    
    return redirect('admin_dashboard')