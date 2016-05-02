from rest_framework import serializers
from models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        field = ('id', 'username', 'created_at', 'updated_at',
                  'tagline', 'password', 'confirm_password', 'bucketlists')
        read_only_fields = ('created_at', 'updated_at',)
