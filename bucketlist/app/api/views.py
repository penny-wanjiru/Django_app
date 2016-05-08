from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
     )
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateAPIview(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIview(APIView):
    permissions_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        if serializer.is_valid(raise_exception = True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializers.error, status=HTTP_400_BAD_REQUEST)


