from rest_framework.pagination import (
    PageNumberPagination,
    )


class BucketlistPageNumberPagination(PageNumberPagination):
    page_size = 2 

