from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, ValidationError
import phonenumbers

def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("Enter a valid phone number.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Enter a valid phone number.")

class CustomUser(AbstractUser):
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[
            RegexValidator(regex=r'^\d{11}$', message='CPF must be 11 digits')
        ]
    )
    full_name = models.CharField(max_length=255) 
    full_address = models.TextField()
    phone_number = models.CharField(
        max_length=15, 
        validators=[validate_phone_number]  # Updated to use the custom validator
    )
    
    # Address fields
    street = models.CharField(max_length=255)  
    home_number = models.CharField(max_length=10)  
    city = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    country = models.CharField(max_length=100, default='Brazil')  

    # Set the email field as the unique identifier for the user
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'cpf', 'phone_number', 'street', 'home_number', 'city', 'state', 'country']  \
        
# aq ta definindo uma classe chamada filial, que representa uma tabela no banco de dados
# A a classe passa como parametro "models.Model", que Ã© a classe base para todos os modelos em django
class Filial(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)
    data_abertura = models.DateField()

   
    def __str__(self): # aq ele transformna o objeto Filial pra string
        return self.nome #ai aqui vai retornar o nome da filial que a gente colocou antes