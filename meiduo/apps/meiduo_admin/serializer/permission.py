from rest_framework import serializers
from django.contrib.auth.models import Permission,ContentType


class PermissionSerializer(serializers.ModelSerializer):


    class Meta:

        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = ContentType
        fields = ('id','name')