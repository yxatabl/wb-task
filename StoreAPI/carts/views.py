from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import CartItemSerializer, CartSerializer
from .services import CartService


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CartService.get_or_create_cart(self.request.user)


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item = CartService.add_to_cart(
            user=request.user,
            product_id=serializer.validated_data['product_id'],
            quantity=serializer.validated_data['quantity']
        )

        return cart_item


class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CartService.remove_from_cart(serializer.validated_data['id'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CartService.update_cart_item_quantity(serializer.validated_data['id'], serializer.validated_data['quantity'])