from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from .services import CartService

from drf_spectacular.utils import extend_schema, OpenApiExample


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Получить корзину пользователя",
        description="Возвращает текущую корзину авторизованного пользователя",
        responses={200: CartSerializer},
        tags=['cart'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return CartService.get_or_create_cart(self.request.user)


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cart = CartService.get_or_create_cart(self.request.user)
        return cart.items.all().order_by('id')
    
    @extend_schema(
        summary="Список товаров в корзине",
        description="Возвращает все товары в корзине пользователя",
        tags=['cart'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Добавить товар в корзину",
        description="Добавляет товар в корзину или увеличивает его количество",
        request=AddToCartSerializer,
        responses={201: CartItemSerializer},
        tags=['cart'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'product_id': 1, 'quantity': 2},
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
    
    @extend_schema(
        summary="Получить элемент корзины",
        description="Возвращает конкретный товар из корзины по ID",
        tags=['cart'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Обновить количество товара",
        description="Изменяет количество товара в корзине",
        tags=['cart'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        summary="Удалить товар из корзины",
        description="Удаляет товар из корзины",
        tags=['cart'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)