from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pagination_class = None

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['username'] = user.username
        token['phone'] = user.user_fields_by_type.phone

        return token
