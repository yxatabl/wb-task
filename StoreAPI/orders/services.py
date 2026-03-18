from users.models import User
from carts.models import Cart, CartItem
from .models import Order, OrderItem


class OrderService:
    @staticmethod
    def create_order(user : User):
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        order_total_price = sum(item.product.price*item.quantity for item in cart_items)
        if order_total_price > user.balance:
            raise ValueError("Insufficient balance to create the order")
        
        for item in cart_items:
            if item.quantity > item.product.quantity:
                raise ValueError(f"Not enough stock for product {item.product.name}")
            
        order = Order.objects.create(user=user)

        user.balance -= order_total_price
        user.save()

        for item in cart_items:
            item.product.quantity -= item.quantity
            item.product.save()
            
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        
        cart.delete()
        
        return order