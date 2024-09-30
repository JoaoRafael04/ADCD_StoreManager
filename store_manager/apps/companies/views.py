from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Branch, Company

@login_required
def company_list(request):
    # Show only companies that belong to the logged-in user
    companies = Company.objects.filter(user=request.user)
    return render(request, 'company_list.html', {'companies': companies})

@login_required
def company_detail(request, company_id):
    # Ensure the user can only access their own companies
    company = get_object_or_404(Company, id=company_id, user=request.user)
    branches = Branch.objects.filter(company=company)  # Show branches for this company
    return render(request, 'company_detail.html', {'company': company, 'branches': branches})

@login_required
def branch_list(request, company_id):
    # Fetch the company using the provided company_id
    company = get_object_or_404(Company, id=company_id)
    # Fetch branches related to this company
    branches = Branch.objects.filter(company=company)

    # Render the branch list template with the company and branches context
    return render(request, 'branch_list.html', {'company': company, 'branches': branches})

@login_required
def branch_detail(request, branch_id):
    # Get branch by ID and ensure the user owns the company this branch belongs to
    branch = get_object_or_404(Branch, id=branch_id, company__user=request.user)
    return render(request, 'branch_detail.html', {'branch': branch})

@login_required
def register_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sector = request.POST.get('sector')
        description = request.POST.get('description')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')  # Handling file uploads

        # Basic validation
        if not name or not sector or not email:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'register_company.html')

        # Create and save the new company
        company = Company(
            name=name,
            sector=sector,
            description=description,
            email=email,
            photo=photo,
            user=request.user  # Automatically link the company to the logged-in user
        )
        company.save()

        messages.success(request, 'Company registered successfully!')
        return redirect('company_list')

    return render(request, 'register_company.html')

@login_required
def register_branch(request, company_id=None):
    if request.method == 'POST':
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        website = request.POST.get('website')
        description = request.POST.get('description')
        
        company = get_object_or_404(Company, id=company_id, user=request.user)

        # Basic validation
        if not name or not cnpj or not email:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'register_branch.html', {'company': company})

        # Create and save the new branch
        branch = Branch(
            name=name,
            cnpj=cnpj,
            address=address,
            phone_number=phone_number,
            email=email,
            website=website,
            description=description,
            company=company  # Automatically link the branch to the selected company
        )
        branch.save()

        messages.success(request, 'Branch registered successfully!')
        return redirect('branch_list', company_id=company.id)

    else:
        company = get_object_or_404(Company, id=company_id, user=request.user)
        return render(request, 'register_branch.html', {'company': company})