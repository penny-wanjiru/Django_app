from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination
)


class BucketlistPageNumberPagination(PageNumberPagination):
    page_size = 2


class BucketlistLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 2
