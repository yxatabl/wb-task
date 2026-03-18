from django.urls import path

from users.views import (
    UserDetailView, 
    UserLoginView, 
    UserRegistrationView, 
    UserBalanceUpdateView
)

urlpatterns = [
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('user/balance/', UserBalanceUpdateView.as_view(), name='user-balance'),
    path('user/register/', UserRegistrationView.as_view(), name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
]