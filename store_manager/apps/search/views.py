from django.http import JsonResponse
from products.models import Product
from companies.models import Branch

def search_product(request):
    product_name = request.GET.get('product_name')
    branch_id = request.GET.get('branch_id')
    
    branch = Branch.objects.get(id=branch_id)
    product = Product.objects.filter(name__icontains=product_name, branch=branch).first()

    if product:
        response = {
            'status': 'found',
            'branch': branch.name,
            'product': product.name,
            'quantity': product.quantity
        }
    else:
        other_branches = Branch.objects.exclude(id=branch_id)
        for other_branch in other_branches:
            product = Product.objects.filter(name__icontains=product_name, branch=other_branch).first()
            if product:
                response = {
                    'status': 'available_in_other_branch',
                    'branch': other_branch.name,
                    'product': product.name,
                    'quantity': product.quantity
                }
                break
        else:
            response = {'status': 'not_found'}

    return JsonResponse(response)