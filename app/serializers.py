from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemItem
        fields = '__all__'


class RecommendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedItem
        fields = '__all__'


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        exclude = ['id']
