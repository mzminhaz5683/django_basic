from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status

from lib import constants as const
from lib.error import errormessage, errorutil
from lib.validationresponse import ValidationResponse
from apps.testapi.validations import passwordchecker

def canUserSignup(signupSerializerIn):
	email = signupSerializerIn.validated_data[const.EMAIL_PROPERTY]
	password = signupSerializerIn.validated_data[const.PASSWORD_PROPERTY]
	if not passwordchecker.isStrongPassword(password):
		return errorutil.get400Error(errormessage.WEAK_PASSWORD_ERROR, False)
	retypePassword = \
		signupSerializerIn.validated_data[const.RETYPE_PASSWORD_PROPERTY]
	isExistUser = User.objects.filter(username__iexact=email).exists()
	if isExistUser:
		return errorutil.getSingleErrorResponse(
			errormessage.EMAIL_EXISTS_ERROR, False, status.HTTP_409_CONFLICT
		)
	if password != retypePassword:
		return errorutil.get400Error(errormessage.DISCORD_PASSWORD_ERROR, False)
	return ValidationResponse(True, None, None)

def canUserLogin(loginSerializerIn):
	email = loginSerializerIn.validated_data[const.EMAIL_PROPERTY].lower()
	password = loginSerializerIn.validated_data[const.PASSWORD_PROPERTY]
	user = authenticate(username=email, password=password)
	if not user:
		return errorutil.get401Error(
			errormessage.INVALID_EMAIL_OR_PASSWORD_ERROR, False
		)
	return ValidationResponse(True, user, None)
