from rest_framework import serializers
from .models import Profile, Tag, Question, Comment

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'image', 'user')
        extra_kwargs = {
            'name': {'write_only': True}
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'data_create', 'rating', 'author', 'tags']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'data_create', 'author', 'question', 'correct_status']