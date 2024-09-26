from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'home.html') 

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Supondo que 'password' é o campo de senha no seu formulário
            user.save()
            login(request, user)  # Loga o usuário imediatamente após o registro
            messages.success(request, 'Registration successful!')  # Mensagem de sucesso
            return redirect('control_painel')  # Redireciona para a página inicial
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')  # Mensagem de sucesso
                return redirect('control_painel')  # Redireciona para a página inicial
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Logic for sending password reset email
            send_mail(
                'Password Reset Request',
                'Click the link below to reset your password:',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,  # Para depuração, ajuste conforme necessário
            )
            messages.success(request, 'Password reset email sent!')  # Mensagem de sucesso
            return render(request, 'accounts/password_reset_done.html')
        else:
            messages.error(request, 'No user with this email address.')  # Mensagem de erro
    return render(request, 'accounts/password_reset.html')

from django.contrib.auth.decorators import login_required
@login_required
def control_painel_view(request):
    return render(request, 'accounts/control_painel.html')





# views.py
from django.shortcuts import render, redirect
from .models import Filial

def cadastrar_filial(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')  # Usando get() para evitar o erro
        endereco = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        telefone = request.POST.get('telefone')
        data_abertura = request.POST.get('data_abertura')

        # Verifique se algum campo obrigatório é None ou vazio
        if not nome or not endereco or not cidade or not estado or not telefone or not data_abertura:
            # Lide com o erro, como retornar uma mensagem de erro
            return render(request, 'accounts/cadastro_filial.html', {'error': 'Todos os campos são obrigatórios!'})

        # Criação da nova filial
        nova_filial = Filial(
            nome=nome,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            telefone=telefone,
            data_abertura=data_abertura
        )
        nova_filial.save()
        
        return redirect('control_painel')
    
    return render(request, 'accounts/cadastro_filial.html')

# View para listar todas as filiais cadastradas
def listar_filiais(request):
    # Busca todas as filiais no banco de dados
    filiais = Filial.objects.all()
    
    # ai a gente chama o render aqui e renderiza o template e passa a lista de filiais como contexto
    return render(request, 'accounts/control_painel.html', {'filiais': filiais})
