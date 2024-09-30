from django.urls import path
from . import views

urlpatterns = [
    path('categories/register/<int:branch_id>/', views.register_category, name='register_category'),  # Register category
    path('branches/<int:branch_id>/categories/', views.category_list, name='category_list'),  # List categories for a branch
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),  # Category detail with slug
]
