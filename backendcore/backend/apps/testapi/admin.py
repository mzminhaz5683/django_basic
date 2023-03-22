from django.contrib import admin

from apps.testapi.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'userUuid',
		'userName',
		'userEmail',
		'userProfile',
		'profileCreateTime',
		'joinDate',
		'agreementExpiryDate',
		'profileBalance',
		'isDeleted'
	]

admin.site.register(Profile, ProfileAdmin)
