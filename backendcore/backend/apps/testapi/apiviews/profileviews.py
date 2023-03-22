import logging
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from lib.error import errorutil, errormessage
from lib.error.exceptionlogger import logException
from apps.testapi.controllers import profilecontroller

logger = logging.getLogger('django')

class UserProfile(APIView):
	permission_classes = (AllowAny,)

	def post(self, request, token, format=None): # ............................. add Profile Picture
		apiResponse = None
		try:
			apiResponse = profilecontroller.addProfilePicture(request, token)
		except Exception as exception:
			apiResponse = errorutil.get500Error(exception)
		return JsonResponse(apiResponse.response, status=apiResponse.status)
