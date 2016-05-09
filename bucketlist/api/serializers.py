from rest_framework.serializers import ModelSerializer
from app.models import BucketList, BucketListItem




class BucketlistItemSerializer(ModelSerializer):
    """Define bucketlistitems serializer fields."""

    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'done', 'bucketlist',
                  'date_created', 'date_updated')
        read_only_fields = ('id', 'date_created', 'date_updated')

class BucketlistSerializer(ModelSerializer):
    items = BucketlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = BucketList
        fields = ['id', 'user', 'name', 'items', 'date_created', 'date_updated']
        read_only_fields = ('id', 'user', 'date_created', 'date_updated', 'items')


# class BucketlistDetailSerializer(ModelSerializer):
#     items = BucketlistItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = BucketList
#         fields = ['id', 'user', 'name', 'items', 'date_created', 'date_updated']


# class BucketlistCreateUpdateSerializer(ModelSerializer):
#     class Meta:
#         model = BucketList
#         fields = ['name']


