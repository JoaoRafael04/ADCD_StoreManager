from django.urls import path
from . import views

urlpatterns = [
    path('register/company/', views.register_company, name='register_company'),
    path('register/branch/<int:company_id>/', views.register_branch, name='register_branch'),
    
    # Company list and detail
    path('companies/', views.company_list, name='company_list'),
    path('companies/register/', views.register_company, name='register_company'),
    path('companies/<int:company_id>/branches/', views.branch_list, name='branch_list'),
    path('companies/<int:company_id>/branches/register/', views.register_branch, name='register_branch'),  # Register branch
    
    
    # Branch list and detail
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/<int:branch_id>/', views.branch_detail, name='branch_detail'),
]
