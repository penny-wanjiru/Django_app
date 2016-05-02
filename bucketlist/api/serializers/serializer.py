from rest_framework import serializers
from models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        field = ('id', 'firstname', 'lastname', 'created', 'modified',
                  'tagline', 'password', 'confirm_password', 'bucketlists')
        read_only_fields = ('created', 'modified',)
