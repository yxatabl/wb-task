from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product

from decimal import Decimal

User = get_user_model()


class ProductTests(APITestCase):
    
    def setUp(self):
        # Создаем обычного пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            balance=Decimal('1000.00')
        )
        
        # Создаем админа
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            balance=Decimal('1000.00')
        )
        
        # Создаем тестовые товары
        self.product1 = Product.objects.create(
            name='Product 1',
            description='Description 1',
            price=Decimal('99.99'),
            quantity=10
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            description='Description 2',
            price=Decimal('149.99'),
            quantity=5
        )
        
        # URL-адреса
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product1.id])
    
    def test_get_all_products_unauthenticated(self):
        """Неавторизованный пользователь может видеть список товаров"""
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_get_all_products_authenticated(self):
        """Авторизованный пользователь может видеть список товаров"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_get_single_product(self):
        """Получение одного товара"""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)
        self.assertEqual(response.data['price'], '99.99')
    
    def test_create_product_as_admin(self):
        """Админ может создать товар"""
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '299.99',
            'quantity': 15
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.last().name, 'New Product')
    
    def test_create_product_as_regular_user(self):
        """Обычный пользователь НЕ может создать товар"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '299.99',
            'stock': 15
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2)
    
    def test_create_product_unauthenticated(self):
        """Неавторизованный пользователь НЕ может создать товар"""
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '299.99',
            'stock': 15
        }
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_product_as_admin(self):
        """Админ может обновить товар"""
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'Updated Name', 'price': '199.99'}
        response = self.client.patch(self.product_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Name')
        self.assertEqual(self.product1.price, Decimal('199.99'))
    
    def test_update_product_as_regular_user(self):
        """Обычный пользователь НЕ может обновить товар"""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Name'}
        response = self.client.patch(self.product_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_product_as_admin(self):
        """Админ может удалить товар"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_delete_product_as_regular_user(self):
        """Обычный пользователь НЕ может удалить товар"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2)