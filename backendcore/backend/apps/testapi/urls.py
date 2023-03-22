from django.urls import path

from apps.testapi import apiendpoints
from apps.testapi.apiviews import authviews, profileviews

urlpatterns = [
	path(apiendpoints.USERS, authviews.Users.as_view(), name='users'),
	path(apiendpoints.AUTHENTICATIONS, authviews.Authonticate.as_view(), name='auths'),
	path(apiendpoints.TOKENS, authviews.UserToken.as_view(), name='token'),
	path(apiendpoints.PROFILES, profileviews.UserProfile.as_view(), name='profiles'),
]


'''
postman requests:
	1. head ==> Token Authorization:
		a. url: http://<host_ip>:8000/api/v1/auths
		b. headers: dictionary{Authorization: 'TOKEN 5e17e5177dd0aadacef53808bed1d2e74062c4f9'}

	2. delete ==> logout (Delete Token):
		a. url: http://<host_ip>:8000/api/v1/auths/<token_key>

	3. post ==> login (Token creation & user login):
		a. url: http://<host_ip>:8000/api/v1/auths
		b. body-json: dictionary{"email": "1@test.com", "password": "12345aA$"}

	4. post ==> signup (user creation):
		a. url: http://<host_ip>:8000/api/v1/users
		b. body-json: dictionary{"email": "1@test.com", "password": "12345aA$", "retypePassword": "12345aA$"}

	5. post ==> updateProfile (upload photo):
		a. url: http://<host_ip>:8000/api/v1/profiles/<token_key>
		b. body-formData: File{'profilePicture': <image_file>}
'''