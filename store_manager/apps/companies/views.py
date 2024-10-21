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
def edit_company(request, company_id):
    company = get_object_or_404(Company, id=company_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        sector = request.POST.get('sector')
        description = request.POST.get('description')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')  # For handling file uploads

        # Basic validation
        if not all([name, sector, description, email]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'edit_company.html', {'company': company})

        # Update company data
        company.name = name
        company.sector = sector
        company.description = description
        company.email = email

        # Only update photo if a new one is uploaded
        if photo:
            company.photo = photo
            
        company.save()

        messages.success(request, 'Empresa atualizada com sucesso!')
        return redirect('company_detail', company_id=company.id)

    # Render the company edit template with the current company data
    return render(request, 'edit_company.html', {'company': company})

@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id, user=request.user)

    if request.method == 'POST':
        # Delete the company and all related branches
        company.delete()
        messages.success(request, 'Empresa excluída com sucesso!')
        return redirect('company_list')

    return render(request, 'delete_company.html', {'company': company})

#Branch -------------------------------------------------

@login_required
def branch_list(request, company_id):
    # Fetch the company using the provided company_id and ensure the user owns it
    company = get_object_or_404(Company, id=company_id, user=request.user)

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
    
@login_required
def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id, company__user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        website = request.POST.get('website')
        description = request.POST.get('description')

        # Basic validation
        if not all([name, cnpj, address, phone_number, email, website, description]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'edit_branch.html', {'branch': branch})

        # Update branch data
        branch.name = name
        branch.cnpj = cnpj
        branch.address = address
        branch.phone_number = phone_number
        branch.email = email
        branch.website = website
        branch.description = description
        branch.save()

        messages.success(request, 'Filial atualizada com sucesso!')
        return redirect('branch_detail', branch_id=branch.id)

    # Render the branch edit template with the current branch data
    return render(request, 'edit_branch.html', {'branch': branch})

@login_required
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == 'POST':
        branch.delete()
        messages.success(request, 'Branch deleted successfully!')
        return redirect('branch_list', company_id=branch.company.id)  # Redirect after deletion

    return render(request, 'delete_branch.html', {'branch': branch})