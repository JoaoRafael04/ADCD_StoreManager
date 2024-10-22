from django.test import TestCase
from .models import Category, Subcategory, Product
from apps.companies.models import Branch, Company
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from datetime import date

class CategorySubcategoryProductModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        
        # Cria uma instância de Company
        self.company_data = {
            'name': 'Test Company',
            'sector': 'Technology',
            'description': 'A company that specializes in technology.',
            'email': 'company@example.com',
            'user': self.user, 
        }

        self.company = Company.objects.create(**self.company_data)

        # Agora cria a Branch associada a essa Company
        self.branch = Branch.objects.create(
            company=self.company,
            name="Test Branch",
            cnpj='12.345.678/0001-90',
            address='123 Test St',
            phone_number='+5511999999999',
            email='branch@example.com',
            website='https://branch.example.com',
            description='A test branch description'
        )

        # Dados da categoria
        self.category_data = {
            'name': 'Electronics',
            'description': 'Category for electronic products',
            'branch': self.branch
        }

        # Criando uma categoria
        self.category = Category.objects.create(**self.category_data)

        # Dados da subcategoria
        self.subcategory_data = {
            'name': 'Smartphones',
            'category': self.category
        }

        # Criando uma subcategoria
        self.subcategory = Subcategory.objects.create(**self.subcategory_data)

        # Dados do produto
        self.product_data = {
            'name': 'iPhone',
            'sku': 'IPHONE12',
            'price': 999.99,
            'quantity': 50,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': 'Apple',
            'expiration_date': None,
            'characteristics': {'color': 'Black', 'memory': '128GB'}
        }

        # Criando um produto
        self.product = Product.objects.create(**self.product_data)

    # Teste de criação de categoria
    def test_create_category(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Category for electronic products')
        self.assertEqual(self.category.branch, self.branch)
        self.assertEqual(self.category.slug, slugify('Electronics'))

    # Teste de criação de subcategoria
    def test_create_subcategory(self):
        self.assertEqual(self.subcategory.name, 'Smartphones')
        self.assertEqual(self.subcategory.category, self.category)

    # Teste de criação de produto
    def test_create_product(self):
        self.assertEqual(self.product.name, 'iPhone')
        self.assertEqual(self.product.sku, 'IPHONE12')
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.quantity, 50)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.subcategory, self.subcategory)
        self.assertEqual(self.product.brand, 'Apple')
        self.assertIsNone(self.product.expiration_date)
        self.assertEqual(self.product.characteristics, {'color': 'Black', 'memory': '128GB'})

    # Teste de representação de string
    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_subcategory_str(self):
        self.assertEqual(str(self.subcategory), 'Smartphones')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'iPhone')

    # Testando se o campo slug é gerado automaticamente
    def test_slug_field(self):
        self.assertEqual(self.category.slug, 'electronics')
        # Modificando o nome da categoria e verificando o slug
        self.category.name = 'Home Appliances'
        self.category.save()
        self.assertEqual(self.category.slug, slugify('Home Appliances'))

    # Testando a exclusão de categoria com subcategoria e produtos
    def test_category_delete_cascade(self):
        self.category.delete()
        with self.assertRaises(Subcategory.DoesNotExist):
            Subcategory.objects.get(pk=self.subcategory.pk)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product.pk)
