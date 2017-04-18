from rest_framework.pagination import (
    LimitOffsetPagination
)


class BucketlistLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 7
