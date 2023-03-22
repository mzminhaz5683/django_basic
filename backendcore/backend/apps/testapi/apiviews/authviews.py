import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ParseError

from lib.error import errorutil, errormessage
from lib.error.exceptionlogger import logException
from apps.testapi.controllers import authusercontroller, authtokencontroller
from apps.testapi.restframework.authorization import \
	TokenAuthenticationWithExpiration

logger = logging.getLogger('django')

class Users(APIView):
	permission_classes = (AllowAny,)

	def post(self, request, format=None): # ................................................. signup
		apiResponse = None
		try:
			apiResponse = authusercontroller.userSignup(request)
		except ParseError as exception:
			apiResponse = errorutil.getJSONParseError(exception)
		except Exception as exception:
			apiResponse = errorutil.get500Error(exception)
		return JsonResponse(apiResponse.response, status=apiResponse.status)

class Authonticate(APIView):
	permission_classes = (AllowAny,)

	def head(self, request, format=None): # ..................................... token expiry check
		statusCode = None
		try:
			TokenAuthenticationWithExpiration.authenticate(
				TokenAuthenticationWithExpiration(), request=request
			)
			statusCode = authtokencontroller.checkAuthorization(request)
		except Exception as exception:
			statusCode = status.HTTP_401_UNAUTHORIZED
			logException(logger, None, errormessage.INVALID_TOKEN_ERROR)
		return Response(status=statusCode)

	def post(self, request, format=None): # .................................................. login
		apiResponse = None
		try:
			apiResponse = authusercontroller.authenticateUser(request)
		except ParseError as exception:
			apiResponse = errorutil.getJSONParseError(exception)
		except Exception as exception:
			apiResponse = errorutil.get500Error(exception)
		return JsonResponse(apiResponse.response, status=apiResponse.status)

class UserToken(APIView):
	permission_classes = (AllowAny,)

	def delete(self, request, token, format=None): # ........................................ logout
		statusCode = None
		try:
			statusCode = authtokencontroller.deleteToken(token)
		except Exception as exception:
			statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
			logException(logger, exception, errormessage.INTERNAL_SERVER_ERROR)
		return Response(status=statusCode)
