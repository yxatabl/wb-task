from rest_framework import generics, permissions

from .models import Product
from .serializers import ProductSerializer

from drf_spectacular.utils import extend_schema


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Список товаров",
        description="Возвращает список всех товаров (доступно всем)",
        tags=['products'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Создать товар",
        description="Создает новый товар (только для администраторов)",
        tags=['products'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary="Получить товар",
        description="Возвращает информацию о конкретном товаре",
        tags=['products'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Обновить товар",
        description="Обновляет информацию о товаре (только для администраторов)",
        tags=['products'],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        summary="Удалить товар",
        description="Удаляет товар (только для администраторов)",
        tags=['products'],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)