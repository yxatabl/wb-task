import logging

from users.models import User

from carts.models import Cart, CartItem

from .models import Order, OrderItem
from .exceptions import EmptyCartError, InsufficientBalanceError, InsufficientStockError

from django.db import transaction

logger = logging.getLogger('orders')


class OrderService:
    @staticmethod
    def create_order(user : User):
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if len(cart_items) == 0:
            raise EmptyCartError("Cart is empty")

        order_total_price = sum(item.product.price*item.quantity for item in cart_items)
        if order_total_price > user.balance:
            raise InsufficientBalanceError("Insufficient balance to create the order")
        
        for item in cart_items:
            if item.quantity > item.product.quantity:
                raise InsufficientStockError(f"Not enough stock for product {item.product.name}")

        with transaction.atomic():            
            order = Order.objects.create(user=user)

            user.balance -= order_total_price
            user.save()

            for item in cart_items:
                item.product.quantity -= item.quantity
                item.product.save()
                
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            
            cart.delete()

            logger.info(msg='created order', extra={'order_id': order.id})
            
            return order