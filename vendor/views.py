from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import VendorProfile, VendorApplication
from .forms import VendorApplicationForm, VendorProfileForm
from sales.models import Sale, CommissionWithdrawal, SaleSubmission
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import json


def home(request):
    return render(request, 'index.html')

def thanks(request):
    return render(request, 'thanks.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            
            # If "remember me" is not checked, set session to expire when browser closes
            if not remember_me:
                request.session.set_expiry(0)
            
            # Check if user is staff/admin
            if user.is_staff:
                return redirect('admin_dashboard')
            
            try:
                # Check if user is a vendor
                vendor = VendorProfile.objects.get(user=user)
                if vendor.is_approved:
                    return redirect('vendor_dashboard')
                else:
                    messages.warning(request, 'Your vendor account is pending approval.')
                    return redirect('login')
            except VendorProfile.DoesNotExist:
                messages.error(request, 'You do not have a vendor profile.')
                return redirect('become_vendor')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('login')

def become_vendor(request):
    if request.method == 'POST':
        form = VendorApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = VendorApplicationForm()
    return render(request, 'become_vendor.html', {'form': form})

@login_required
def vendor_dashboard(request):
    vendor = VendorProfile.objects.get(user=request.user)
    
    # Get all sales
    sales = Sale.objects.filter(vendor=vendor)
    
    # Calculate total items sold and revenue
    total_items = sales.aggregate(Sum('items_sold'))['items_sold__sum'] or 0
    total_revenue = sales.aggregate(Sum('amount'))['amount__sum'] or 0
    total_commission = sales.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
    
    # Get pending sales submissions
    pending_submissions = SaleSubmission.objects.filter(
        vendor=vendor,
        status='PENDING'
    ).order_by('-submitted_at')
    
    # Get recent sales (last 10)
    recent_sales = sales.order_by('-created_at')[:10]
    
    # Get pending withdrawals count
    pending_withdrawals = CommissionWithdrawal.objects.filter(
        vendor=vendor, 
        status='PENDING'
    ).count()
    
    context = {
        'vendor': vendor,
        'total_items': total_items,
        'total_revenue': total_revenue,
        'total_commission': total_commission,
        'pending_submissions': pending_submissions,
        'recent_sales': recent_sales,
        'pending_withdrawals': pending_withdrawals,
    }
    
    return render(request, 'vendor_dash.html', context)

@login_required
@staff_member_required
def admin_dashboard(request):
    # Existing stats
    total_vendors = VendorProfile.objects.count()
    total_sales = Sale.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    # New stats
    total_items = Sale.objects.aggregate(Sum('items_sold'))['items_sold__sum'] or 0
    pending_applications = VendorApplication.objects.filter(is_approved=False).count()
    pending_withdrawals = CommissionWithdrawal.objects.filter(status='PENDING').count()
    pending_sales = SaleSubmission.objects.filter(status='PENDING').order_by('-submitted_at')

    vendors = VendorProfile.objects.all().select_related('user')
    for vendor in vendors:
        vendor.total_sales = Sale.objects.filter(vendor=vendor).aggregate(Sum('amount'))['amount__sum'] or 0

    pending_applications_list = VendorApplication.objects.filter(is_approved=False).order_by('-created_at')
    pending_withdrawals_list = CommissionWithdrawal.objects.filter(status='PENDING').order_by('-request_date')

    context = {
        'total_vendors': total_vendors,
        'total_sales': total_sales,
        'total_items': total_items,
        'pending_applications': pending_applications,
        'pending_withdrawals': pending_withdrawals,
        'pending_sales': pending_sales,
        'vendors': vendors,
        'pending_applications_list': pending_applications_list,
        'pending_withdrawals_list': pending_withdrawals_list,
    }
    
    return render(request, 'admin_dash.html', context)

# @staff_member_required
# def admin_dashboard(request):
#     total_sales = Sale.objects.aggregate(Sum('amount'))['amount__sum'] or 0
#     vendors = VendorProfile.objects.all()
#     pending_applications = VendorApplication.objects.filter(is_approved=False).count()
#     pending_withdrawals = CommissionWithdrawal.objects.filter(status='PENDING').count()
    
#     context = {
#         'total_sales': total_sales,
#         'vendors': vendors,
#         'pending_applications': pending_applications,
#         'pending_withdrawals': pending_withdrawals,
#     }
#     return render(request, 'admin_dash.html', context)

@login_required
def request_withdrawal(request):
    vendor = VendorProfile.objects.get(user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        CommissionWithdrawal.objects.create(
            vendor=vendor,
            amount=amount,
            status='PENDING'
        )
        return redirect('vendor_dashboard')
    return render(request, 'request_withdrawal.html')

@staff_member_required
def process_withdrawal(request, withdrawal_id):
    withdrawal = CommissionWithdrawal.objects.get(id=withdrawal_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        withdrawal.status = status
        withdrawal.processed_date = timezone.now()
        withdrawal.save()
    return redirect('admin_dashboard')


def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('vendor_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# URL pattern decorator to ensure only approved vendors can access vendor dashboard
def vendor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            vendor = VendorProfile.objects.get(user=request.user)
            if not vendor.is_approved:
                messages.warning(request, 'Your vendor account is pending approval.')
                return redirect('login')
        except VendorProfile.DoesNotExist:
            messages.error(request, 'You do not have a vendor profile.')
            return redirect('become_vendor')
        return view_func(request, *args, **kwargs)
    return _wrapped_view






# API Views for AJAX calls
@login_required
@staff_member_required
def update_commission(request, vendor_id):
    if request.method == 'POST':
        vendor = get_object_or_404(VendorProfile, id=vendor_id)
        try:
            commission_rate = Decimal(request.POST.get('commission_rate', '0'))
            vendor.commission_rate = commission_rate
            vendor.save()
            
            sales = Sale.objects.filter(vendor=vendor)
            for sale in sales:
                sale.commission_amount = (sale.amount * commission_rate)/100
                sale.save()
                
            return JsonResponse({'status': 'success', 'message': 'Commission rate updated successfully'})
        except (ValueError, TypeError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponseBadRequest('Invalid request method')

@require_POST
@staff_member_required
def approve_application(request, application_id):
    try:
        application = get_object_or_404(VendorApplication, id=application_id)
        
        # Create user account
        user = User.objects.create_user(
            username=application.email,
            email=application.email,
            first_name=application.full_name.split()[0],
            last_name=' '.join(application.full_name.split()[1:]) if len(application.full_name.split()) > 1 else ''
        )
        
        # Create vendor profile
        vendor = VendorProfile.objects.create(
            user=user,
            business_name=application.business_name,
            phone=application.phone,
            is_approved=True
        )
        
        # Mark application as approved
        application.is_approved = True
        application.save()
        
        # TODO: Send approval email to vendor
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@staff_member_required
def reject_application(request, application_id):
    try:
        application = get_object_or_404(VendorApplication, id=application_id)
        application.delete()
        # TODO: Send rejection email to applicant
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@staff_member_required
def approve_withdrawal(request, withdrawal_id):
    try:
        withdrawal = get_object_or_404(CommissionWithdrawal, id=withdrawal_id)
        withdrawal.status = 'APPROVED'
        withdrawal.processed_date = timezone.now()
        withdrawal.save()
        # TODO: Trigger payment processing
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
@staff_member_required
def reject_withdrawal(request, withdrawal_id):
    try:
        withdrawal = get_object_or_404(CommissionWithdrawal, id=withdrawal_id)
        withdrawal.status = 'DENIED'
        withdrawal.processed_date = timezone.now()
        withdrawal.save()
        # TODO: Send notification to vendor
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

# from decimal import Decimal
# from django.http import JsonResponse, HttpResponseBadRequest

# @login_required
# @staff_member_required
# def update_commission(request, vendor_id):
#     if request.method == 'POST':
#         vendor = get_object_or_404(VendorProfile, id=vendor_id)
#         try:
#             commission_rate = Decimal(request.POST.get('commission_rate', '0'))
#             vendor.commission_rate = commission_rate
#             vendor.save()
#             return JsonResponse({'status': 'success', 'message': 'Commission rate updated successfully'})
#         except (ValueError, TypeError) as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return HttpResponseBadRequest('Invalid request method')

@login_required
@staff_member_required
def update_item_rate(request, vendor_id):
    if request.method == 'POST':
        vendor = get_object_or_404(VendorProfile, id=vendor_id)
        try:
            item_rate = Decimal(request.POST.get('item_rate', '0'))
            vendor.item_rate = item_rate
            vendor.save()
            
            # Update all sales amounts for this vendor based on the new item rate
            sales = Sale.objects.filter(vendor=vendor)
            for sale in sales:
                sale.amount = sale.items_sold * item_rate
                sale.save()
            
            # Recalculate total sales after updating individual sales
            total_sales = sales.aggregate(Sum('amount'))['amount__sum'] or 0
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item rate updated successfully',
                'total_sales': float(total_sales),
                'new_rate': float(item_rate)
            })
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return HttpResponseBadRequest('Invalid request method')