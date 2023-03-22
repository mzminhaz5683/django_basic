import logging
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from lib.error import errorutil
from lib import constants as const
from lib.apiresponse import ApiResponse
from apps.testapi.validations import uservalidation
from apps.testapi.serializers.loginserializer import LoginSerializerIn
from apps.testapi.serializers.singupserializer import SignupSerializerIn
from apps.testapi.restframework.authorization import \
	TokenAuthenticationWithExpiration

logger = logging.getLogger('django')

def authenticateUser(request):
	loginSerializerIn = LoginSerializerIn(data=request.data)
	if not loginSerializerIn.is_valid():
		return errorutil.getSerilizerError(loginSerializerIn.errors)
	loginValidation = uservalidation.canUserLogin(loginSerializerIn)
	if not loginValidation.isValid:
		return loginValidation
	token, _ = Token.objects.get_or_create(user=loginValidation.response)
	try:
		TokenAuthenticationWithExpiration.authenticate_credentials(
			TokenAuthenticationWithExpiration(), key=token.key
		)
	except Exception as e:
		token.delete()
		token, _ = Token.objects.get_or_create(user=loginValidation.response)
	response = {'token': token.key, 'timestamp': token.created}
	return ApiResponse(response, status=status.HTTP_200_OK)

def signup(signupSerializerIn):
	username = email = \
		signupSerializerIn.validated_data[const.EMAIL_PROPERTY].lower()
	password = signupSerializerIn.validated_data[const.PASSWORD_PROPERTY]
	user = User.objects.create_user(username, email, password)
	return ApiResponse({}, status.HTTP_201_CREATED)

def userSignup(request):
	signupSerializerIn = SignupSerializerIn(data=request.data)
	if signupSerializerIn.is_valid():
		signupValidation = uservalidation.canUserSignup(signupSerializerIn)
		if signupValidation.isValid:
			with transaction.atomic():
				return signup(signupSerializerIn)
		return ApiResponse(signupValidation.response, signupValidation.status)
	return errorutil.getSerilizerError(signupSerializerIn.errors)
