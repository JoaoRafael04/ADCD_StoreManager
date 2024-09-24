from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='company_photos/', blank=True, null=True)
    email = models.EmailField()

class Branch(models.Model):
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)