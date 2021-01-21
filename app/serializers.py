from rest_framework import serializers
from .models import Profile, Tag, Question, Comment

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'nick', 'image', 'user')
        extra_kwargs = {
            'nick': {'write_only': True}
        }