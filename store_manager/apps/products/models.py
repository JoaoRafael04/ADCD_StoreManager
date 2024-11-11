from django.db import models
from django.utils.text import slugify
from datetime import datetime
from apps.companies.models import Branch

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use name to create a base slug
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use name and related category slug to create a base slug
            base_slug = f"{slugify(self.category.name)}-{slugify(self.name)}"
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while Subcategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

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
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use name and SKU to create a base slug
            base_slug = f"{slugify(self.name)}-{slugify(self.sku)}"
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name