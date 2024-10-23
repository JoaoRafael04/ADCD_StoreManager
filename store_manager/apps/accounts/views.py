from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import CustomUser

def home(request):
    return render(request, 'home.html')

@login_required
def menu(request):
    # Your view logic here
    return render(request, 'menu.html')

@login_required
def logoff(request):
    logout(request)
    messages.success(request, 'Você foi desconectado!')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_Name')
        cpf = request.POST.get('cpf')
        phone_number = request.POST.get('phone_number')
        street = request.POST.get('street')
        home_number = request.POST.get('home_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        # Basic validation
        if not email or not username or not password:
            messages.error(request, 'Por favor preencha todos os campos obrigatórios.')
            return render(request, 'accounts/register.html')

        # Create user
        try:
            user = CustomUser(
                email=email,
                username=username,
                full_Name=full_name,
                cpf=cpf,
                phone_number=phone_number,
                street=street,
                home_number=home_number,
                city=city,
                state=state,
                country=country,
            )
            user.set_password(password)  # Hash the password
            user.full_clean()  # Validate the model fields
            user.save()

            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('menu')  # Ensure 'menu' URL is correctly defined

        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'accounts/register.html')

        except IntegrityError:
            messages.error(request, 'A user with this email or username already exists.')
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('menu')  # Ensure 'menu' URL is correctly defined
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')  # Render login page with error message

    return render(request, 'accounts/login.html')
