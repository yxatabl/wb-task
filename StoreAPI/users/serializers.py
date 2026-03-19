from rest_framework import serializers

from .models import User

from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'balance']

        read_only_fields = ('id', 'balance')


class UserBalanceUpdateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    
    class Meta:
        model = User
        fields = ('id', 'balance', 'amount')

    def update(self, instance : User, validated_data):
        amount = validated_data.pop('amount', 0)

        instance.balance += amount
        instance.save()

        return instance
    
    def validate(self, attrs):
        if attrs['amount'] <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0"})
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'password')
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must provide username and password')