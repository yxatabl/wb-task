from django.urls import path
from users.views import UserList, UserDetails, UserUpdateBalance

urlpatterns = [
    path('users/', UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('users/<int:pk>/addBalance', UserUpdateBalance.as_view(), name='user-addBalance')
]