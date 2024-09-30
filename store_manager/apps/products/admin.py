from django.contrib import admin
from .models import Category, Subcategory, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'description')
    search_fields = ('name', 'description')
    list_filter = ('branch',)
    ordering = ('name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally filter the queryset for specific user roles
        # if request.user.is_superuser:
        #     return qs
        return qs

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity', 'category', 'subcategory', 'brand', 'expiration_date')
    search_fields = ('name', 'sku', 'brand')
    list_filter = ('category', 'subcategory', 'brand', 'expiration_date')
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally filter the queryset for specific user roles
        # if request.user.is_superuser:
        #     return qs
        return qs