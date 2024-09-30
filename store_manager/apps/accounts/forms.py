""" import requests
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    cep = forms.CharField(max_length=9, label='CEP')

    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'cpf', 'cep', 'street', 
            'home_number', 'city', 'state', 'country', 'email', 
            'phone_number', 'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        cep = cleaned_data.get("cep")

        # Validate passwords
        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        # Verify CEP with Correios API
        if cep:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            if response.status_code == 200:
                address_data = response.json()
                if 'erro' in address_data:
                    raise ValidationError("Invalid CEP")
                else:
                    # Fill in address details from API response
                    cleaned_data['street'] = address_data.get('logradouro', '')
                    cleaned_data['city'] = address_data.get('localidade', '')
                    cleaned_data['state'] = address_data.get('uf', '')
                    cleaned_data['country'] = "Brazil"
            else:
                raise ValidationError("Failed to validate CEP")

        return cleaned_data
 """