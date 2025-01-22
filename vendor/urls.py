from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('thanks/', views.home, name='thanks'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/withdrawal/request/', views.request_withdrawal, name='request_withdrawal'),
    path('admin/withdrawal/process/<int:withdrawal_id>/', views.process_withdrawal, name='process_withdrawal'),
    path('login/', views.login_view, name='login'),
    # path('api/update-commission/<int:vendor_id>/', views.update_commission, name='update_commission'),
    path('api/approve-application/<int:application_id>/', views.approve_application, name='approve_application'),
    path('api/reject-application/<int:application_id>/', views.reject_application, name='reject_application'),
    path('api/approve-withdrawal/<int:withdrawal_id>/', views.approve_withdrawal, name='approve_withdrawal'),
    path('api/reject-withdrawal/<int:withdrawal_id>/', views.reject_withdrawal, name='reject_withdrawal'),
    path('update-commission/<int:vendor_id>/', views.update_commission, name='update_commission'),
    path('update-item-rate/<int:vendor_id>/', views.update_item_rate, name='update_item_rate'),
]