import logging
from rest_framework.authtoken.models import Token
from rest_framework import status

logger = logging.getLogger('django')

def deleteToken(token):
	if (token):
		token = Token.objects.filter(key=token).delete()
		return status.HTTP_204_NO_CONTENT
	return status.HTTP_404_NOT_FOUND

def checkAuthorization(request):
	authorization = request.META.get('HTTP_AUTHORIZATION')
	if isinstance(authorization, str):
		try:
			authorizationKey = authorization.split(" ")[1]
		except IndexError:
			return status.HTTP_400_BAD_REQUEST
		isAuthorized = Token.objects.filter(key=authorizationKey).exists()
		if isAuthorized:
			return status.HTTP_204_NO_CONTENT
	return status.HTTP_401_UNAUTHORIZED
