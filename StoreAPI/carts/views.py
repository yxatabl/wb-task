from rest_framework import generics, permissions

from .serializers import CartSerializer, CartItemSerializer
from .services import CartService


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CartService.get_or_create_cart(self.request.user)


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cart = CartService.get_or_create_cart(self.request.user)
        return cart.items.all()
    
    def perform_create(self, serializer):
        cart = CartService.get_or_create_cart(self.request.user)
        serializer.save(cart=cart)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cart = CartService.get_or_create_cart(self.request.user)
        return cart.items.all()