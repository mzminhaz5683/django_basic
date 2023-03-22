import os, copy
from rest_framework import status

from config.localconfig import wwwConfig
from lib.apiresponse import ApiResponse
from lib.error import errormessage, errorlib, errorutil
from apps.testapi.models import Profile
from apps.testapi.serializers.profileserializer import ProfileSerializerIn

def getUpdatedProfile(profile, request):
	print(request.user) # ------------------------------------------------------ gives authonticate user
	updatedProfile = copy.deepcopy(profile)
	requestProfilePicture = request.FILES.get('profilePicture')
	if (requestProfilePicture):
		if (profile.userProfile.name):
			os.remove(wwwConfig['MEDIA_ROOT'] + profile.userProfile.name) # ---- remove file from media folder
		updatedProfile.userProfile = requestProfilePicture
	return updatedProfile

def addProfilePicture(request, token):
	profileSerializerIn = ProfileSerializerIn(data=request.data)
	if not profileSerializerIn.is_valid():
		return errorutil.getSerilizerError(profileSerializerIn.errors)
	mediaUrl = wwwConfig['BASE_URL'] + wwwConfig['MEDIA_URL'] # ---------------- http://0.0.0.0:8000/media/
	try:
		response = {'profilePicture': None}
		profile, _ = Profile.objects.get_or_create(userName='mz', userEmail='1@test.com')
		profile = getUpdatedProfile(profile, request)
		profile.save()
		if (profile.userProfile):
			response['profilePicture'] = mediaUrl + profile.userProfile.name # - http://0.0.0.0:8000/media/<file>
		return ApiResponse(response, status=status.HTTP_200_OK)
	except Exception as error:
		print(error)
		return errorlib.get409Error(errormessage.INTERNAL_SERVER_ERROR, True)
