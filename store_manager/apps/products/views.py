from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Subcategory, Product
from apps.companies.models import Branch, Company
import json


# List all categories for a specific branch
@login_required
def category_list(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    categories = Category.objects.filter(branch=branch)

    if not categories.exists():
        messages.info(request, f"No categories found for {branch.name}.")

    return render(request, 'category_list.html', {'branch': branch, 'categories': categories})


# View details of a specific category
@login_required
def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'category_detail.html', {'category': category})


# Register a new category under a specific branch
@login_required
def register_category(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, 'Please provide a name for the category.')
            return render(request, 'register_category.html', {'branch': branch})

        if Category.objects.filter(name=name, branch=branch).exists():
            messages.error(request, 'A category with this name already exists in this branch.')
            return render(request, 'register_category.html', {'branch': branch})

        category = Category(name=name, description=description, branch=branch)
        category.save()

        messages.success(request, 'Category registered successfully!')
        return redirect('category_list', branch_id=branch.id)

    return render(request, 'register_category.html', {'branch': branch})


# Edit an existing category
@login_required
def edit_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, 'Please provide a name for the category.')
            return render(request, 'edit_category.html', {'category': category})

        category.name = name
        category.description = description
        category.save()

        messages.success(request, 'Category updated successfully!')
        return redirect('category_detail', category_slug=category.slug)

    return render(request, 'edit_category.html', {'category': category})


# Delete a category
@login_required
def delete_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    branch_id = category.branch.id

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list', branch_id=branch_id)

    return render(request, 'delete_category.html', {'category': category})


# List all subcategories for a specific category
@login_required
def subcategory_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Subcategory.objects.filter(category=category)

    if not subcategories.exists():
        messages.info(request, f"No subcategories found for {category.name}.")

    return render(request, 'subcategory_list.html', {'category': category, 'subcategories': subcategories})


# View details of a specific subcategory
@login_required
def subcategory_detail(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
    return render(request, 'subcategory_detail.html', {'subcategory': subcategory})


# Register a new subcategory under a specific category
@login_required
def register_subcategory(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Please provide a name for the subcategory.')
            return render(request, 'register_subcategory.html', {'category': category})

        if Subcategory.objects.filter(name=name, category=category).exists():
            messages.error(request, 'A subcategory with this name already exists in this category.')
            return render(request, 'register_subcategory.html', {'category': category})

        subcategory = Subcategory(name=name, category=category)
        subcategory.save()

        messages.success(request, 'Subcategory registered successfully!')
        return redirect('subcategory_list', category_slug=category.slug)

    return render(request, 'register_subcategory.html', {'category': category})


# Edit an existing subcategory
@login_required
def edit_subcategory(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Please provide a name for the subcategory.')
            return render(request, 'edit_subcategory.html', {'subcategory': subcategory})

        subcategory.name = name
        subcategory.save()

        messages.success(request, 'Subcategory updated successfully!')
        return redirect('subcategory_detail', subcategory_slug=subcategory.slug)

    return render(request, 'edit_subcategory.html', {'subcategory': subcategory})


# Delete a subcategory
@login_required
def delete_subcategory(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
    category_slug = subcategory.category.slug

    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully!')
        return redirect('subcategory_list', category_slug=category_slug)

    return render(request, 'delete_subcategory.html', {'subcategory': subcategory})


# List all products for a specific subcategory
@login_required
def product_list(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
    products = Product.objects.filter(subcategory=subcategory)

    if not products.exists():
        messages.info(request, f"No products found for {subcategory.name}.")

    return render(request, 'product_list.html', {'subcategory': subcategory, 'products': products})


# View to display the details of a specific product
@login_required
def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'product_details.html', {'product': product})


# Register a new product under a specific subcategory
@login_required
def register_product(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        brand = request.POST.get('brand')
        expiration_date = request.POST.get('expiration_date')
        characteristics = request.POST.get('characteristics')

        if not name or not sku or not price or not quantity:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'register_product.html', {'subcategory': subcategory})

        if expiration_date:
            try:
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                return render(request, 'register_product.html', {'subcategory': subcategory})
        else:
            expiration_date = None

        product = Product(
            name=name,
            sku=sku,
            price=price,
            quantity=quantity,
            brand=brand,
            expiration_date=expiration_date,
            characteristics=characteristics,
            category=subcategory.category,
            subcategory=subcategory
        )
        product.save()

        messages.success(request, 'Product registered successfully!')
        return redirect('product_list', subcategory_slug=subcategory.slug)

    return render(request, 'register_product.html', {'subcategory': subcategory})


# Edit an existing product
@login_required
def edit_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        brand = request.POST.get('brand')
        expiration_date = request.POST.get('expiration_date')
        characteristics = request.POST.get('characteristics')

        if not name or not sku or not price or not quantity or not brand:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'edit_product.html', {'product': product})

        if expiration_date:
            try:
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                return render(request, 'edit_product.html', {'product': product})
        else:
            expiration_date = None

        product.name = name
        product.sku = sku
        product.price = price
        product.quantity = quantity
        product.brand = brand
        product.expiration_date = expiration_date
        product.characteristics = characteristics
        product.save()

        messages.success(request, 'Product updated successfully!')
        return redirect('product_detail', product_slug=product.slug)

    return render(request, 'edit_product.html', {'product': product})


# Delete a product
@login_required
def delete_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    subcategory_slug = product.subcategory.slug

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list', subcategory_slug=subcategory_slug)

    return render(request, 'delete_product.html', {'product': product})
