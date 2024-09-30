from django.test import TestCase
from .models import Product, Category, Subcategory

class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Electronic devices")
        self.subcategory = Subcategory.objects.create(name="Mobile Phones", category=self.category)
        self.product = Product.objects.create(
            name="iPhone", sku="12345", price=999.99, quantity=50, 
            category=self.category, subcategory=self.subcategory, brand="Apple"
        )

    def test_product_creation(self):
        product = Product.objects.get(name="iPhone")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.quantity, 50)
        self.assertEqual(product.brand, "Apple")

    def test_product_sku(self):
        product = Product.objects.get(name="iPhone")
        self.assertEqual(product.sku, "12345")