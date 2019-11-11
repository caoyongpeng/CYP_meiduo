import re
from rest_framework import serializers

from apps.users.models import User


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 20,
                'min_length': 8,
                'required':False
            },
            'username': {
                'max_length': 20,
                'min_length': 4
            }
        }

    # 验证手机号格式
    def validate_mobile(self, attrs):
        """
        :param attrs: 获取手机号值
        :return:
        """
        if not re.match(r'1[3-9]\d{9}', attrs):
            raise serializers.ValidationError('手机格式不正确')

        return attrs

    # 重写保存业务，完成密码加密
    def create(self, validated_data):
        # 1、调用父类保存方法，获取保存后的用户对象
        user = super().create(validated_data)
        # 2、使用用户对象中的加密方法进行加密操作
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.save()

        return user

    def update(self, instance, validated_data):
        instance = super().update(instance,validated_data)

        password = validated_data.get('password')

        if password:
            instance.set_password(validated_data['password'])
            instance.save()
        return instance