from  rest_framework.generics import ListAPIView
from app.models import BucketList, BucketListItem


class BucketListAPIview(ListAPIView):
    queryset = BucketList.objects.all()