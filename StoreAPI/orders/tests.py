from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from carts.models import Cart
from .models import Order, OrderItem
from .exceptions import InsufficientBalanceError, InsufficientStockError, EmptyCartError
from products.models import Product

User = get_user_model()


class OrderListCreateViewTests(TestCase):
    """Тесты для OrderListCreateView"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.user.balance = 1000
        self.user.save()
            
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        self.product1 = Product.objects.create(
            name="Test Product 1",
            description="Description for product 1",
            price=100.00,
            quantity=10
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            description="Description for product 2",
            price=200.00,
            quantity=5
        )

        self.cart = Cart.objects.create(user=self.user)
        self.cart.items.create(product=self.product1, quantity=2)
        self.cart.items.create(product=self.product2, quantity=1)
        
        self.order1 = Order.objects.create(user=self.user)

        self.cart_other = Cart.objects.create(user=self.other_user)
        self.cart_other.items.create(product=self.product1, quantity=1)
        self.cart_other.items.create(product=self.product2, quantity=2)
        self.order_other = Order.objects.create(user=self.other_user)
        
        self.url = reverse('order-list')
    
    def test_list_orders_unauthenticated(self):
        """Тест получения списка заказов неаутентифицированным пользователем"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('orders.services.OrderService.create_order')
    def test_create_order_success(self, mock_create_order):
        """Тест успешного создания заказа"""
        self.client.force_authenticate(user=self.user)
        
        mock_order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=mock_order,
            product_id=self.product1.id,
            quantity=2
        )
        OrderItem.objects.create(
            order=mock_order,
            product_id=self.product2.id,
            quantity=1
        )
        mock_create_order.return_value = mock_order
        
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_create_order.assert_called_once_with(self.user)
        
        self.assertIn('id', response.data)
        self.assertIn('order_items', response.data)
        self.assertEqual(len(response.data['order_items']), 2)
    
    @patch('orders.services.OrderService.create_order')
    def test_create_order_empty_cart(self, mock_create_order):
        """Тест создания заказа с пустой корзиной"""
        self.client.force_authenticate(user=self.user)
        
        self.cart.items.all().delete()
        
        mock_create_order.side_effect = EmptyCartError("Cart is empty")
        
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Cart is empty")
    
    @patch('orders.services.OrderService.create_order')
    def test_create_order_insufficient_stock(self, mock_create_order):
        """Тест создания заказа при недостаточном количестве товара"""
        self.client.force_authenticate(user=self.user)
        
        mock_create_order.side_effect = InsufficientStockError(
            f"Insufficient stock for product {self.product1.name}"
        )
        
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn("Insufficient stock", response.data['error'])
    
    @patch('orders.services.OrderService.create_order')
    def test_create_order_insufficient_balance(self, mock_create_order):
        """Тест создания заказа при недостаточном балансе"""
        self.client.force_authenticate(user=self.user)
        
        mock_create_order.side_effect = InsufficientBalanceError(
            "Insufficient balance"
        )
        
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Insufficient balance")
    
    def test_create_order_unauthenticated(self):
        """Тест создания заказа неаутентифицированным пользователем"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_serializer_class_selection(self):
        """Тест выбора правильного сериализатора"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with patch('orders.services.OrderService.create_order'):
            response = self.client.post(self.url, {})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderDetailViewTests(TestCase):
    """Тесты для OrderDetailView"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        self.product = Product.objects.create(
            name="Test Product",
            description="Description for product",
            price=100.00,
            quantity=10
        )
        
        self.order = Order.objects.create(user=self.user)
        OrderItem.objects.create(
            order=self.order,
            product_id=self.product.id,
            quantity=2
        )
        
        self.other_order = Order.objects.create(user=self.other_user)
        
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})
        self.other_url = reverse('order-detail', kwargs={'pk': self.other_order.id})
    
    def test_retrieve_order_authenticated_owner(self):
        """Тест получения конкретного заказа владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(len(response.data['order_items']), 1)
        self.assertEqual(response.data['order_items'][0]['product_id'], self.product.id)
        self.assertEqual(response.data['order_items'][0]['quantity'], 2)
    
    def test_retrieve_order_authenticated_not_owner(self):
        """Тест получения заказа пользователем, не являющимся владельцем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.other_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_order_unauthenticated(self):
        """Тест получения заказа неаутентифицированным пользователем"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_nonexistent_order(self):
        """Тест получения несуществующего заказа"""
        self.client.force_authenticate(user=self.user)
        url = reverse('order-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
