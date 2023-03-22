from rest_framework import serializers

class LoginSerializerIn(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
