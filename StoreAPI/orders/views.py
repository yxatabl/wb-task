from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import OrderSerializer
from .services import OrderService
from .models import Order


class OrdersView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            OrderSerializer(Order.objects.filter(user=request.user), many=True).data,
            status=status.HTTP_200_OK
        )


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = OrderService.create_order(request.user)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
