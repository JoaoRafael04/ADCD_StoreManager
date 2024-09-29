from django.shortcuts import render, redirect
from .models import Produtos

def adicionar_produto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        marca = request.POST['marca']
        producao = request.POST['producao']
        frete_gratis = request.POST.get('frete_gratis', 'off') == 'on'
        altura = request.POST['altura']
        largura = request.POST['largura']
        profundidade = request.POST['profundidade']
        itens_para_caixa = request.POST.get('itens_para_caixa', 'off') == 'on'
        unidade_medida = request.POST['unidade_medida']
        validade = request.POST['validade']
        
        # Criar um novo objeto de produto
        novo_produto = Produtos.objects.create(
            nome=nome,
            marca=marca,
            producao=producao,
            frete_gratis=frete_gratis,
            altura=altura,
            largura=largura,
            profundidade=profundidade,
            itens_para_caixa=itens_para_caixa,
            unidade_medida=unidade_medida,
            validade=validade
        )
        
        return redirect('lista_produtos')  # Redirecionar para uma lista de produtos, por exemplo

    return render(request, 'products/adicionar_produto.html')  # Verifique o caminho do template

def lista_produtos(request):
    produtos = Produtos.objects.all()
    return render(request, 'products/lista_produtos.html', {'produtos': produtos})




