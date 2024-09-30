from django.urls import path
from . import views

urlpatterns = [
    path('register/company/', views.register_company, name='register_company'),
    path('companies/', views.company_list, name='company_list'),  # Company list
    path('companies/<int:company_id>/detail/', views.company_detail, name='company_detail'),  # Company detail

    # Branches
    path('companies/<int:company_id>/branches/register/', views.register_branch, name='register_branch'),  # Register branch
    path('companies/<int:company_id>/branches/', views.branch_list, name='branch_list'),  # Branch list
    path('branches/<int:branch_id>/detail/', views.branch_detail, name='branch_detail'),  # Branch detail
]
