from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from decimal import Decimal

User = get_user_model()


class UserTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            balance=Decimal('1000.00')
        )
        
        self.user_detail_url = reverse('user-detail')
        self.user_balance_url = reverse('user-balance')
        self.user_register_url = reverse('user-register')
        self.user_login_url = reverse('user-login')
    
    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
        }
        response = self.client.post(self.user_register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(User.objects.count(), 2)
    
    def test_user_registration_duplicate_username(self):
        """Тест регистрации с существующим username"""
        data = {
            'username': 'testuser',
            'password': 'newpass123'
        }
        response = self.client.post(self.user_register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """Тест входа пользователя"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.user_login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_user_login_invalid_credentials(self):
        """Тест входа с неверными данными"""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.user_login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_info_authenticated(self):
        """Авторизованный пользователь может получить свои данные"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['balance'], '1000.00')
    
    def test_get_user_info_unauthenticated(self):
        """Неавторизованный пользователь не может получить данные"""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_balance_authenticated(self):
        """Авторизованный пользователь может пополнить баланс"""
        self.client.force_authenticate(user=self.user)
        data = {'amount': '500.00'}
        response = self.client.post(self.user_balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, Decimal('1500.00'))
    
    def test_update_balance_negative_amount(self):
        """Пополнение на отрицательную сумму"""
        self.client.force_authenticate(user=self.user)
        data = {'amount': '-100.00'}
        response = self.client.post(self.user_balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_balance_unauthenticated(self):
        """Неавторизованный пользователь не может пополнить баланс"""
        data = {'amount': '500.00'}
        response = self.client.post(self.user_balance_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)