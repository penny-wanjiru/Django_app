from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )


class BucketlistLimitOffsetPagination(LimitOffsetPagination):
    default_limit  = 2
    max_limit = 2


class BucketlistPageNumberPagination(PageNumberPagination):
    page_size = 2 

