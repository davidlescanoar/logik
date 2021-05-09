from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ProblemItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemItem
        fields = ["puntaje"]