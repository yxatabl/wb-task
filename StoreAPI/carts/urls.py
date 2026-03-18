from django.urls import path

from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/addItem', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/removeItem', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/updateItem', UpdateCartItemView.as_view(), name='update-item')
]