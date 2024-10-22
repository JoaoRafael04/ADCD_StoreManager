from django.urls import path
from . import views

urlpatterns = [
    path('register/company/', views.register_company, name='register_company'), # Register company
    path('companies/', views.company_list, name='company_list'),  # Company list
    path('companies/<int:company_id>/detail/', views.company_detail, name='company_detail'),  # Company detail
    path('companies/<int:company_id>/edit/', views.edit_company, name='edit_company'),  # Edit company
    path('companies/<int:company_id>/delete/', views.delete_company, name='delete_company'),  # Delete company

    # Branches
    path('companies/<int:company_id>/branches/register/', views.register_branch, name='register_branch'),  # Register branch
    path('companies/<int:company_id>/branches/', views.branch_list, name='branch_list'),  # Branch list
    path('branches/<int:branch_id>/detail/', views.branch_detail, name='branch_detail'),  # Branch detail
    path('branches/<int:branch_id>/edit/', views.edit_branch, name='edit_branch'),  # Edit branch
    path('branches/<int:branch_id>/delete/', views.delete_branch, name='delete_branch'),  # Delete branch

]
