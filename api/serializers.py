from rest_framework import serializers

from api import models


class UserSerializer(serializers.ModelSerializer):
    today_cost = serializers.SerializerMethodField()
    put_in = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        exclude = ['id', 'password']
