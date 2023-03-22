from rest_framework import serializers
from lib import constants as const

class SignupSerializerIn(serializers.Serializer):
	email = serializers.EmailField(max_length=const.USERNAME_MAX_LENGTH)
	password = serializers.CharField(
		min_length=const.PASSWORD_MIN_LENGTH,
		max_length=const.PASSWORD_MAX_LENGTH
	)
	retypePassword = serializers.CharField(
		min_length=const.PASSWORD_MIN_LENGTH,
		max_length=const.PASSWORD_MAX_LENGTH
	)
