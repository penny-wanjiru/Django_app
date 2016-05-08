from rest_framework.serializers import (ModelSerializer, CharField, EmailField)
from app.models import BucketList
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
    username = CharField(required=False, allow_blank=True)
    email = EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'token']

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data["password"]
        if not email and not username:
            raise ValidationError("You must provide auth username and email")

            user = User.objects.filter(
                   Q(email=email)|
                   Q(username=username)
                ).distinct()
            if user.exists() and user.count() == 1:
                user = user.first()
            else:
                raise ValidationError("This username/email is not valid")
            if user_obj:
                if not user_obj.check_password(password):
                    raise ValidationError("Incorrect credentials please try again")
            data['token'] = "SOME TOKEN"

        return data
