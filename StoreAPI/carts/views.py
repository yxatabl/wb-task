from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
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
        return cart.items.all().order_by('id')
    
    def create(self, request, *args, **kwargs):
        add_serializer = AddToCartSerializer(data=request.data)
        add_serializer.is_valid(raise_exception=True)
        
        cart_item = CartService.add_to_cart(
            user=request.user,
            product_id=add_serializer.validated_data['product_id'],
            quantity=add_serializer.validated_data['quantity']
        )
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cart = CartService.get_or_create_cart(self.request.user)
        return cart.items.all().order_by('id')