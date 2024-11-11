from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Subcategory, Product
from apps.companies.models import Branch, Company
import json

# View to list all categories for a specific branch
@login_required
def category_list(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    categories = Category.objects.filter(branch=branch)

    if not categories.exists():
        messages.info(request, f"No categories found for {branch.name}.")

    return render(request, 'category_list.html', {'branch': branch, 'categories': categories})



@login_required
def category_detail(request, slug):
    try:
        # Fetch the category by slug instead of ID
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        # Show a friendly message if the category is not found
        messages.error(request, "Sorry, this category does not exist.")
        return redirect('category_list')  # Redirect to the list of categories

    # Render the detail page for the category
    return render(request, 'category_detail.html', {'category': category})

# View to register a new category under a specific branch
@login_required
def register_category(request, branch_id):
    user_companies = Company.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Fetch the branch and ensure the user is authorized to access it
        branch = get_object_or_404(Branch, id=branch_id, company__user=request.user)

        # Basic validation for required fields
        if not name or not description:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'register_category.html', {'branch': branch, 'companies': user_companies})

        # Check if a category with the same name already exists in this branch
        if Category.objects.filter(name=name, branch=branch).exists():
            messages.error(request, 'A category with this name already exists in this branch.')
            return render(request, 'register_category.html', {'branch': branch, 'companies': user_companies})

        # Create and save the new category
        category = Category(
            name=name,
            description=description,
            branch=branch
        )
        category.save()

        messages.success(request, 'Category registered successfully!')
        return redirect('category_list', branch_id=branch.id)

    else:
        # Display the form if the request method is GET
        branch = get_object_or_404(Branch, id=branch_id, company__user=request.user)
        return render(request, 'register_category.html', {'branch': branch, 'companies': user_companies})

@login_required
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate fields
        if not name or not description:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'edit_category.html', {'category': category})

        # Update the category
        category.name = name
        category.description = description
        category.save()

        messages.success(request, 'Category updated successfully!')
        return redirect('category_detail', slug=category.slug)  # Use slug here

    return render(request, 'edit_category.html', {'category': category})

@login_required
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    branch_id = category.branch.id  # Get the branch ID from the category

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list', branch_id=branch_id)  # Pass the branch_id here

    return render(request, 'delete_category.html', {'category': category})

# View to list all subcategories for a specific category
@login_required
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)

    if not subcategories.exists():
        messages.info(request, f"No subcategories found for {category.name}.")

    return render(request, 'subcategory_list.html', {'category': category, 'subcategories': subcategories})

# View to registar a new subcategory for a specific category
@login_required
def register_subcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Please enter a name for the subcategory.')
            return render(request, 'register_subcategory.html', {'category': category})

        if Subcategory.objects.filter(name=name, category=category).exists():
            messages.error(request, 'A subcategory with this name already exists.')
            return render(request, 'register_subcategory.html', {'category': category})

        subcategory = Subcategory(name=name, category=category)
        subcategory.save()

        messages.success(request, 'Subcategory registered successfully!')
        return redirect('subcategory_list', category_id=category.id)

    return render(request, 'register_subcategory.html', {'category': category})

@login_required
def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    return render(request, 'subcategory_detail.html', {'subcategory': subcategory})

@login_required
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Please enter a name for the subcategory.')
            return render(request, 'edit_subcategory.html', {'subcategory': subcategory})

        subcategory.name = name
        subcategory.save()
        messages.success(request, 'Subcategory updated successfully!')
        return redirect('subcategory_detail', subcategory_id=subcategory.id)

    return render(request, 'edit_subcategory.html', {'subcategory': subcategory})

@login_required
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    category_id = subcategory.category.id

    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully!')
        return redirect('subcategory_list', category_id=category_id)

    return render(request, 'delete_subcategory.html', {'subcategory': subcategory})

@login_required
def product_list(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    products = Product.objects.filter(subcategory=subcategory)
    
    # Converte o campo `characteristics` para JSON
    for product in products:
        if isinstance(product.characteristics, str):
            product.characteristics = json.loads(product.characteristics)

    return render(request, 'product_list.html', {
        'subcategory': subcategory,
        'products': products
    })

@login_required
def add_product(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        brand = request.POST.get('brand')
        expiration_date = request.POST.get('expiration_date')
        characteristics = request.POST.get('characteristics')

        # Validação simples dos campos
        if not name or not sku or not price or not quantity:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'add_product.html', {'subcategory': subcategory})

        # Criação do produto
        product = Product(
            name=name,
            sku=sku,
            price=price,
            quantity=quantity,
            subcategory=subcategory,
            category=subcategory.category,  # Define a categoria automaticamente
            brand=brand,
            expiration_date=expiration_date,
            characteristics=characteristics
        )
        product.save()

        messages.success(request, 'Product added successfully!')
        return redirect('product_list', subcategory_id=subcategory.id)

    return render(request, 'add_product.html', {'subcategory': subcategory})

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Verifica se as características são uma string JSON e as converte
    if isinstance(product.characteristics, str):
        product.characteristics = json.loads(product.characteristics)

    return render(request, 'product_details.html', {'product': product})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.brand = request.POST.get('brand')
        product.expiration_date = request.POST.get('expiration_date')
        
        # Atualizar as características no formato JSON, se fornecidas
        characteristics = request.POST.get('characteristics')
        if characteristics:
            import json
            try:
                product.characteristics = json.loads(characteristics)
            except json.JSONDecodeError:
                messages.error(request, 'Invalid JSON format for characteristics.')
                return render(request, 'edit_product.html', {'product': product})
        
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_details', product_id=product.id)

    return render(request, 'edit_product.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list', subcategory_id=product.subcategory.id)

    return render(request, 'delete_product.html', {'product': product})