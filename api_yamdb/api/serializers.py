from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    confirmation_code = serializers.CharField(required=False, read_only=True)
    email = serializers.EmailField(required=False)

    # def create(self, validated_data):
    
    #     if 'confirmation_code' in validated_data:
    #         return self.context['request'].user

    class Meta:
        model = User
        fields = ('email', 'username', 'confirmation_code')
