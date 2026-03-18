from django.urls import path
from .views import CreateOrderView, OrdersView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/create', CreateOrderView.as_view(), name='create-order')
]