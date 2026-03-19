from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserBalanceUpdateSerializer, UserLoginSerializer, UserRegistrationSerializer, UserSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Профиль пользователя",
        description="Возвращает информацию о текущем авторизованном пользователе",
        tags=['users'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user


class UserBalanceUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Пополнить баланс",
        description="Увеличивает баланс пользователя на указанную сумму",
        request=UserBalanceUpdateSerializer,
        responses={200: UserSerializer},
        tags=['users'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'amount': 1000.50},
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = UserBalanceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.balance += serializer.validated_data['amount']
        user.save()
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создает нового пользователя и возвращает JWT токены",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        },
        tags=['users'],
        examples=[
            OpenApiExample(
                'Успешная регистрация',
                value={
                    'user': {
                        'id': 1,
                        'username': 'john_doe',
                        'balance': '0.00'
                    },
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        summary="Вход в систему",
        description="Аутентификация пользователя и получение JWT токенов",
        request=UserLoginSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        },
        tags=['users'],
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'username': 'john_doe', 'password': 'securepassword'},
                request_only=True,
            ),
            OpenApiExample(
                'Успешный вход',
                value={
                    'user': {
                        'id': 1,
                        'username': 'john_doe',
                        'balance': '1000.00'
                    },
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })