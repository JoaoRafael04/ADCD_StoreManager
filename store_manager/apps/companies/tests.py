from django.test import TestCase
from .models import Company, Branch
from django.contrib.auth import get_user_model

class CompanyBranchModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

        self.company_data = {
            'name': 'Test Company',
            'sector': 'Technology',
            'description': 'A company that specializes in technology.',
            'email': 'company@example.com',
            'user': self.user, 
        }

        self.company = Company.objects.create(**self.company_data)

        self.branch_data = {
            'name': 'Test Branch',
            'cnpj': '12.345.678/0001-90',
            'address': '123 Test St, Test City',
            'phone_number': '+5511999999999',
            'email': 'branch@example.com',
            'website': 'https://branch.example.com',
            'description': 'A branch of the Test Company.',
            'company': self.company 
        }

        self.branch = Branch.objects.create(**self.branch_data)

    def test_create_company(self):
        self.assertEqual(self.company.name, 'Test Company')
        self.assertEqual(self.company.sector, 'Technology')
        self.assertEqual(self.company.description, 'A company that specializes in technology.')
        self.assertEqual(self.company.email, 'company@example.com')
        self.assertEqual(self.company.user, self.user)

    def test_create_branch(self):
        self.assertEqual(self.branch.name, 'Test Branch')
        self.assertEqual(self.branch.cnpj, '12.345.678/0001-90')
        self.assertEqual(self.branch.address, '123 Test St, Test City')
        self.assertEqual(self.branch.phone_number, '+5511999999999')
        self.assertEqual(self.branch.email, 'branch@example.com')
        self.assertEqual(self.branch.website, 'https://branch.example.com')
        self.assertEqual(self.branch.description, 'A branch of the Test Company.')
        self.assertEqual(self.branch.company, self.company)

    def test_company_str(self):
        self.assertEqual(str(self.company), 'Test Company')

    def test_branch_str(self):
        self.assertEqual(str(self.branch), 'Test Branch')

    def test_company_delete_cascade(self):
        self.company.delete()
        with self.assertRaises(Branch.DoesNotExist):
            Branch.objects.get(pk=self.branch.pk)