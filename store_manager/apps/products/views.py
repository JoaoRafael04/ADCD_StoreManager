from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Subcategory, Product
from apps.companies.models import Branch, Company


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