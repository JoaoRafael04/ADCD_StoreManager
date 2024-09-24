from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    expiration_date = models.DateField(null=True, blank=True)
    characteristics = models.JSONField()  

    def __str__(self):
        return self.name