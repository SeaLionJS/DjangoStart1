from .models import User, UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'status', 'description', 'show_birth_date']



class UserUpdateSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(required=False)

    def update(self, instance, validated_data):
        # логіка оновлення користувача (запису в таблиці UserProfile може не бути)
        pass

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'phone', 'show_email', 'show_phone', 'userprofile')