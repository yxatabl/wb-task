from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderCreateSerializer
from .services import OrderService
from .models import Order
from .exceptions import OrderError

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')
    
    def create(self, request, *args, **kwargs):
        try:
            order = OrderService.create_order(self.request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except OrderError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Список заказов",
        description="Возвращает все заказы текущего пользователя",
        responses={200: OrderSerializer(many=True)},
        tags=['orders'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Создать заказ",
        description="Создает новый заказ из товаров в корзине",
        request=None,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Ошибка создания заказа (недостаточно средств/товаров)")
        },
        tags=['orders'],
        examples=[
            OpenApiExample(
                'Успешный ответ',
                value={
                    'id': 1,
                    'order_items': [
                        {'product_id': 1, 'quantity': 2},
                        {'product_id': 2, 'quantity': 1}
                    ]
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
