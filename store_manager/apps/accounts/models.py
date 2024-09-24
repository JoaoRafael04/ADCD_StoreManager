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
    street_number = models.CharField(max_length=10)  
    city = models.CharField(max_length=100)  
    state = models.CharField(max_length=100)  
    country = models.CharField(max_length=100, default='Brazil')  

    # Set the email field as the unique identifier for the user
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'cpf', 'full_address', 'phone_number', 'street', 'street_number', 'city', 'state', 'country']  