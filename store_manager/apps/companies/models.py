from django.db import models
from django.conf import settings  # Import for referencing the user model

class Company(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='company_photos/', blank=True, null=True)
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the user

    def __str__(self):
        return self.name
class Branch(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Linked to the Company

    def __str__(self):
        return self.name
    