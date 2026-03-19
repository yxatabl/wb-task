from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product

from carts.models import Cart, CartItem

from decimal import Decimal

User = get_user_model()

class CartTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            balance=Decimal('1000.00')
        )
        
        self.user2 = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            balance=Decimal('1000.00')
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            quantity=10
        )
        
        self.product2 = Product.objects.create(
            name='Test Product 2',
            description='Test Description 2',
            price=Decimal('149.99'),
            quantity=5
        )
        
        self.cart_url = reverse('cart-detail')
        self.cart_items_url = reverse('cart-item-list')
    
    def test_get_cart_authenticated(self):
        """Авторизованный пользователь может получить свою корзину"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)
    
    def test_get_cart_unauthenticated(self):
        """Неавторизованный пользователь не может получить корзину"""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_item_to_cart(self):
        """Добавление товара в корзину"""
        self.client.force_authenticate(user=self.user)
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        
        response = self.client.post(self.cart_items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_add_duplicate_item(self):
        """Добавление уже существующего товара увеличивает количество"""
        self.client.force_authenticate(user=self.user)
        
        # Первое добавление
        data = {'product_id': self.product.id, 'quantity': 2}
        response1 = self.client.post(self.cart_items_url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Второе добавление того же товара
        response2 = self.client.post(self.cart_items_url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Проверяем, что количество увеличилось
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        self.assertEqual(cart_item.quantity, 4)  # 2 + 2
    
    def test_list_cart_items(self):
        """Получение списка товаров в корзине"""
        self.client.force_authenticate(user=self.user)
        
        # Добавляем товары
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        
        response = self.client.get(self.cart_items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_update_cart_item(self):
        """Обновление количества товара в корзине"""
        self.client.force_authenticate(user=self.user)
        
        # Добавляем товар
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart, 
            product=self.product, 
            quantity=2
        )
        
        item_url = reverse('cart-item-detail', args=[cart_item.id])
        data = {'quantity': 5}
        response = self.client.patch(item_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_remove_cart_item(self):
        """Удаление товара из корзины"""
        self.client.force_authenticate(user=self.user)
        
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart, 
            product=self.product, 
            quantity=2
        )
        
        item_url = reverse('cart-item-detail', args=[cart_item.id])
        response = self.client.delete(item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart.items.count(), 0)
    
    def test_cannot_modify_other_users_cart(self):
        """Пользователь не может изменять чужую корзину"""
        self.client.force_authenticate(user=self.user)
        
        # Создаем корзину для другого пользователя
        other_cart = Cart.objects.create(user=self.user2)
        other_item = CartItem.objects.create(
            cart=other_cart, 
            product=self.product, 
            quantity=2
        )
        
        # Пытаемся удалить товар из чужой корзины
        item_url = reverse('cart-item-detail', args=[other_item.id])
        response = self.client.delete(item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)