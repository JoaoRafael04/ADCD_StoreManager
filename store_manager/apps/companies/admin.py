from django.contrib import admin
from .models import Company, Branch

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 1  # Number of empty forms to display

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'email', 'user')  # Show these fields in the list view
    search_fields = ('name', 'sector', 'email')  # Allow searching by name, sector, and email
    list_filter = ('sector',)  # Filter companies by sector
    inlines = [BranchInline]  # Inline editing for branches under companies

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'company')  # Show these fields in the list view
    search_fields = ('name', 'cnpj', 'email')  # Allow searching by name, CNPJ, and email
    list_filter = ('company',)  # Filter branches by company

# Register the models with the custom admin settings
admin.site.register(Company, CompanyAdmin)
admin.site.register(Branch, BranchAdmin)