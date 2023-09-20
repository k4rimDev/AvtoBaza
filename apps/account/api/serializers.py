from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework_simplejwt.settings import api_settings

from django.conf import settings

from apps.account import models
from apps.order.api import serializers as orderser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pagination_class = None

    @classmethod
    def get_token(cls, user):
        if user.last_login_time and user.last_login_time > timezone.now():
            raise ValidationError(detail={"message": "User can not login"}, code=401)
        token = super().get_token(user)

        # Update User last_login_time for access only one session
        user.last_login_time = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] + timezone.now()
        # Update User last login for task
        user.last_login = timezone.now()
        user.save()

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        token['phone'] = user.phone

        return token

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    pagination_class = None

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data

class UserBalanceActivitySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    transaction_id = serializers.SerializerMethodField()
    class Meta:
        model = models.UserBalance
        fields = ("balance", "remain_balance", "description", "transaction_type", "created_at",
                  "transaction_id")

    def get_transaction_id(self, obj):
        if obj.order:
            return obj.order.transaction_id
        return None
    
    def get_created_at(self, obj):
        formatted_time = datetime.strftime(
            obj.created_at,
            "%Y-%m-%d %H:%M:%S"
        )
        return formatted_time

class UserBalanceActivityDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    transaction_id = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    class Meta:
        model = models.UserBalance
        fields = ("balance", "remain_balance", "description", "transaction_type", "created_at",
                  "transaction_id", "items")

    def get_transaction_id(self, obj):
        if obj.order:
            return obj.order.transaction_id
        return None
    
    def get_items(self, obj):
        if obj.order:
            serializer = orderser.OrderItemSerializer(obj.order, many=False, 
                                                  context=self.context)
            return [serializer.data]
        return None
    
    def get_created_at(self, obj):
        formatted_time = datetime.strftime(
            obj.created_at,
            "%Y-%m-%d %H:%M:%S"
        )
        return formatted_time
