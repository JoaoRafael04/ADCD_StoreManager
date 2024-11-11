from django.urls import path
from . import views

urlpatterns = [
    path('subcategories/<int:subcategory_id>/products/', views.product_list, name='product_list'),
    path('subcategories/<int:subcategory_id>/products/add/', views.add_product, name='add_product'),
    path('subcategories/<int:subcategory_id>/edit/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/<int:subcategory_id>/delete/', views.delete_subcategory, name='delete_subcategory'),
    path('subcategories/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),
    path('categories/<int:category_id>/subcategories/register/', views.register_subcategory, name='register_subcategory'),
    path('categories/<int:category_id>/subcategories/', views.subcategory_list, name='subcategory_list'),
    path('categories/register/<int:branch_id>/', views.register_category, name='register_category'),
    path('branches/<int:branch_id>/categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('products/categories/<slug:slug>/edit/', views.edit_category, name='edit_category'),
    path('products/categories/<slug:slug>/delete/', views.delete_category, name='delete_category'),
]
