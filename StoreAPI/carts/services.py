from .models import Cart, CartItem

from users.models import User

from products.models import Product


class CartService:
    @staticmethod
    def get_or_create_cart(user : User):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
    
    @staticmethod
    def add_to_cart(user : User, product_id : int, quantity : int = 1):
        cart = CartService.get_or_create_cart(user)
        product = Product.objects.get(id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item
    
    @staticmethod
    def remove_from_cart(user : User, product_id : int):
        cart = CartService.get_or_create_cart(user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    

    @staticmethod
    def update_cart_item_quantity(item_id : int, quantity : int):
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = quantity
        cart_item.save()

        return cart_item