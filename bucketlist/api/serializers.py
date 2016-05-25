from rest_framework.serializers import (ModelSerializer, CharField, EmailField)
from app.models import BucketList, BucketListItem
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user already exists")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'token']

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        email = data.get('email', None)
        password = data["password"]
        if not email and not username:
            raise ValidationError("You must provide username and email")
        user = User.objects.filter(
               Q(email=email)|
               Q(username=username)
            ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        data["token"] = "SOME TOKEN"
        return data



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


