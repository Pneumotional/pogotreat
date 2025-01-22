# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing urls ...
    path('vendor/submit-sales/', views.submit_sales, name='submit_sales'),
    path('admin/pending-sales/', views.pending_sales, name='pending_sales'),
     path('process-sale-submission/<int:submission_id>/', views.process_sale_submission, name='process_sale_submission'),
]