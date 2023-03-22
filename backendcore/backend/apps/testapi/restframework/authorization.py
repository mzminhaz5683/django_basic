from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from lib import constants as const

class TokenAuthenticationWithExpiration(TokenAuthentication):
	def authenticate_credentials(self, key):
		try:
			token = Token.objects.get(key=key)
		except Token.DoesNotExist:
			raise AuthenticationFailed(_('Invalid token'))

		currentTime = datetime.utcnow()
		currentUtcTime = currentTime.replace(tzinfo=timezone.utc)
		if token.created < (currentUtcTime - const.EXPIRY_TIME):
			raise AuthenticationFailed(_('Token has expired'))

		return super().authenticate_credentials(key)
