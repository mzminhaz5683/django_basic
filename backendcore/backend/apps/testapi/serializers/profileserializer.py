from rest_framework import serializers
from lib import serializervalidator, constants as const

class ProfileSerializerIn(serializers.Serializer):
	userName = serializers.CharField(max_length=const.NAME_MAX_LINGTH)
	userProfile = serializers.ImageField(allow_null=True, required=False)
	userEmail = serializers.CharField(
		max_length=const.EMAIL_MAX_LENGTH, allow_null=True, required=False
	)
	joinDate = serializers.CharField(allow_null=True, required=False)
	agreementExpiryDate = serializers.CharField(allow_null=True, required=False)
	profileBalance = serializers.DecimalField(
		max_digits=const.FIELD_MAX_DIGITS,
		decimal_places=const.DECIMAL_PLACES,
		allow_null=True,
		required=False
	)

	def validate_userProfile(self, file):
		return serializervalidator.getImageValidation(file)

	def validate_joinDate(self, value):
		return serializervalidator.getDateTimeValidation(value, "%m%Y") # MMYYYY

	def validate_agreementExpiryDate(self, value):
		return serializervalidator.getDateTimeValidation(value, "%m%Y", True) # MMYYYY

	def validate_profileBalance(self, value):
		return serializervalidator.getAmountValidation(value)
