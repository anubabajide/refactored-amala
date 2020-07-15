from rest_framework import serializers
from .models import Product, Interest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            return user