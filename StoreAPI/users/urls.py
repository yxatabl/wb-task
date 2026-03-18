from django.urls import path

from users.views import UserView, UserLoginView, UserRegistrationView, UserUpdateBalance

urlpatterns = [
    path('user/', UserView.as_view(), name='user-info'),
    path('user/addBalance', UserUpdateBalance.as_view(), name='user-addBalance'),
    path('user/register/', UserRegistrationView.as_view(), name='register'),
    path('user/login/', UserLoginView.as_view(), name='login'),
]