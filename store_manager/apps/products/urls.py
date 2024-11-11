from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/<slug:product_slug>/edit/', views.edit_product, name='edit_product'),
    path('products/<slug:product_slug>/delete/', views.delete_product, name='delete_product'),
    path('products/<slug:product_slug>/details/', views.product_detail, name='product_detail'),

    # Subcategory URLs
    path('subcategories/<slug:subcategory_slug>/products/', views.product_list, name='product_list'),
    path('subcategories/<slug:subcategory_slug>/products/add/', views.register_product, name='register_product'),
    path('subcategories/<slug:subcategory_slug>/edit/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/<slug:subcategory_slug>/delete/', views.delete_subcategory, name='delete_subcategory'),
    path('subcategories/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_detail'),

    # Category and Subcategory URLs
    path('categories/<slug:category_slug>/subcategories/register/', views.register_subcategory, name='register_subcategory'),
    path('categories/<slug:category_slug>/subcategories/', views.subcategory_list, name='subcategory_list'),
    path('categories/register/<int:branch_id>/', views.register_category, name='register_category'),

    # Branch and Category URLs
    path('branches/<int:branch_id>/categories/', views.category_list, name='category_list'),
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/edit/', views.edit_category, name='edit_category'),
    path('categories/<slug:category_slug>/delete/', views.delete_category, name='delete_category'),
]

