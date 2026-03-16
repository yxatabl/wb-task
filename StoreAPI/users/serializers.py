from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'balance']

        read_only_fields = ('id', 'balance')


class UserBalanceUpdateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    
    class Meta:
        model = User
        fields = ['id', 'balance', 'amount']

    def update(self, instance : User, validated_data):
        amount = validated_data.pop('amount', 0)

        instance.balance += amount
        instance.save()

        return instance