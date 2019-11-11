from rest_framework import serializers
from django.contrib.auth.models import Group,Permission


class GroupSerializer(serializers.ModelSerializer):


    class Meta:
        model = Group
        fields = '__all__'


class PermissionGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Permission
        fields = '__all__'