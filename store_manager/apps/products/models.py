from django.db import models
from apps.companies.models import Branch
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Atualizar o slug sempre que o nome for modificado
        if not self.slug or self.name != Category.objects.filter(id=self.id).values_list('name', flat=True).first():
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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