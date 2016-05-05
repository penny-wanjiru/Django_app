from rest_framework.serializers import ModelSerializer
from app.models import BucketList


class BucketlistSerializer(ModelSerializer):
    class Meta:
        model = BucketList
        fields = ['id', 'user','name', 'date_created', 'date_updated']


class BucketlistDetailSerializer(ModelSerializer):
    class Meta:
        model = BucketList
        fields = ['id', 'user','name', 'date_created', 'date_updated']


class BucketlistCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = BucketList
        fields = ['name']

