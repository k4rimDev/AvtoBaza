from django.http import JsonResponse
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.account.api import serializers
from apps.account import models
from apps.order import models as om


class MyTokenObtainPairView(TokenObtainPairView):
    pagination_class = None
    serializer_class = serializers.MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class MyTokenRefreshView(TokenRefreshView):
    pagination_class = None
    serializer_class = serializers.MyTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    allowed_methods = ('GET', 'HEAD', 'POST', )

    def post(self, request):
        try:
            print(request.data)
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomLogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    def post(self, request, *args, **kwargs):
        user = request.user

        user.last_login_time = None
        user.save()

        return JsonResponse({"message": "User logout succesfully!"}, status=status.HTTP_200_OK)

class UserBalanceAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    def get(self, request, *args, **kwargs):
        user = request.user

        balance, _created = models.Balance.objects.get_or_create(
            user=user
        )

        return JsonResponse(
            {"balance": balance.balance},
            status=status.HTTP_200_OK
        )

class UserBalanceActivityAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    def get(self, request, *args, **kwargs):
        user = request.user

        balance = models.UserBalance.objects.filter(
            Q(user=user), ~Q(transaction_type=None),
            ~Q(description=None)
        )

        serializer_class = serializers.UserBalanceActivitySerializer(
            balance, many=True, context={"request": request}
        )

        return Response(serializer_class.data, status=status.HTTP_200_OK)

class UserBalanceActivityDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    def get(self, request, *args, **kwargs):
        transaction_id = self.kwargs.get("transaction_id", None)
        if transaction_id and om.OrderItems.objects.filter(transaction_id=transaction_id).exists():
            user = request.user

            balance = models.UserBalance.objects.filter(
                Q(user=user), ~Q(transaction_type=None),
                ~Q(description=None), Q(order__transaction_id=transaction_id)
            )

            if balance.exists():

                serializer_class = serializers.UserBalanceActivityDetailSerializer(
                    balance.first(), many=False, context={"request": request}
                )

                return Response(serializer_class.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Not found!"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Not found!"}, status=status.HTTP_404_NOT_FOUND)
    