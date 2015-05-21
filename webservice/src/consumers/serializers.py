from rest_framework import serializers
from consumers.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Consumer
        fields = ('id', 'username', 'email', 'phone', 'is_valid')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=10, max_length=10)


class PhoneValidationSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
