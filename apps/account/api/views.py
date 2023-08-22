from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.account.api import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    pagination_class = None
    serializer_class = serializers.MyTokenObtainPairSerializer

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
        