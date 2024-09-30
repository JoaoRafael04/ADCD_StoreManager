from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, ValidationError
import phonenumbers

# Validador de número de telefone
def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("Enter a valid phone number.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Enter a valid phone number.")

class CustomUser(AbstractUser):
    # Campo CPF
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[
            RegexValidator(regex=r'^\d{11}$', message='CPF must be 11 digits')
        ]
    )
    
    # Nome completo
    full_Name = models.CharField(max_length=255)
    
    # Número de telefone
    phone_number = models.CharField(
        max_length=15, 
        validators=[validate_phone_number]  # Validador customizado para telefone
    )

    # Campos de endereço
    street = models.CharField(max_length=255)
    home_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Brazil')

    # Definir email como identificador único
    email = models.EmailField(unique=True)

    # Evitar conflito nos relacionamentos reversos com 'groups' e 'user_permissions'
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set', 
        blank=True, 
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_set', 
        blank=True, 
        help_text="Specific permissions for this user."
    )

    # Configurar campo de autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_Name', 'cpf', 'phone_number', 'street', 'home_number', 'city', 'state', 'country']

    # Método para obter nome completo
    def get_full_name(self):
        return self.full_Name or self.username