from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    BucketlistSerializer,
    BucketlistItemSerializer,
     )

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination)
from .permissions import IsOwnerOrReadOnly
from app.models import BucketList, BucketListItem
from .pagination import BucketlistLimitOffsetPagination, BucketlistPageNumberPagination

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
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.error, status=HTTP_400_BAD_REQUEST)



class BucketListCreateAPIview(CreateAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BucketListAPIview(ListAPIView):
    serializer_class = BucketlistSerializer
    pagination_class = BucketlistPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = BucketList.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)
                ).distinct()
        return queryset_list


class BucketListDetailAPIview(RetrieveAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer


class BucketListUpdateAPIview(UpdateAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BucketListDeleteAPIview(DestroyAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class BucketlistItemUpdateAPIview(UpdateAPIView):
    serializer_class = BucketlistItemSerializer

    def get_queryset(self):
        list_id = self.kwargs['list_id']
        item_id = self.kwargs['pk']
        bucketlistitem = BucketListItem.objects.filter(
            id=item_id, bucketlist=list_id)
        return bucketlistitem


class BucketlistItemAPIview(CreateAPIView):
    serializer_class = BucketlistItemSerializer
    search_fields = ('name', )

    def get_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)


class BucketlistDetailItemAPIview(RetrieveAPIView):
    serializer_class = BucketlistItemSerializer

    def get_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)


class BucketlistDeleteItemAPIview(DestroyAPIView):
    serializer_class = BucketlistItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def delete_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)
