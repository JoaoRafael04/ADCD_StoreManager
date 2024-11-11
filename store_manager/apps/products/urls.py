from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/<slug:product_slug>/edit/', views.edit_product, name='edit_product'),  # edit_product.html
    path('products/<slug:product_slug>/delete/', views.delete_product, name='delete_product'),  # delete_product.html
    path('products/<slug:product_slug>/details/', views.product_detail, name='product_detail'),  # product_detail.html
    path('subcategories/<slug:subcategory_slug>/products/', views.product_list, name='product_list'),  # product_list.html
    path('subcategories/<slug:subcategory_slug>/products/add/', views.register_product, name='register_product'),  # register_product.html

    # Subcategory URLs
    path('subcategories/<slug:subcategory_slug>/edit/', views.edit_subcategory, name='edit_subcategory'),  # edit_subcategory.html
    path('subcategories/<slug:subcategory_slug>/delete/', views.delete_subcategory, name='delete_subcategory'),  # delete_subcategory.html
    path('subcategories/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_detail'),  # subcategory_detail.html

    # Category and Subcategory URLs
    path('categories/<slug:category_slug>/subcategories/register/', views.register_subcategory, name='register_subcategory'),  # register_subcategory.html
    path('categories/<slug:category_slug>/subcategories/', views.subcategory_list, name='subcategory_list'),  # subcategory_list.html
    path('categories/register/<int:branch_id>/', views.register_category, name='register_category'),  # Change to branch_id

    # Branch and Category URLs
    path('branches/<int:branch_id>/categories/', views.category_list, name='category_list'),  # category_list.html
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),  # category_detail.html
    path('categories/<slug:category_slug>/edit/', views.edit_category, name='edit_category'),  # edit_category.html
    path('categories/<slug:category_slug>/delete/', views.delete_category, name='delete_category'),  # delete_category.html
]
