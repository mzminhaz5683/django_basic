import uuid
from django.db import models
from django.contrib.auth.models import User

from lib import constants as const
from lib.model.customfields.nonnegativedecimalfield import NonNegativeDecimalField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.PROTECT)
	userUuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	userName = models.CharField(max_length=const.NAME_MAX_LINGTH)
	userEmail = models.CharField(max_length=const.EMAIL_MAX_LENGTH)
	userProfile = models.ImageField(blank=True, null=True)
	profileCreateTime = models.DateTimeField(auto_now_add=True)
	joinDate = models.DateTimeField(blank=True, null=True)
	agreementExpiryDate = models.DateTimeField(blank=True, null=True)
	profileBalance = NonNegativeDecimalField(
		default=0,
		max_digits=const.FIELD_MAX_DIGITS,
		decimal_places=const.DECIMAL_PLACES
	)
	isDeleted = models.BooleanField(default=False)

	class Meta:
		unique_together = ('userName', 'userEmail')

	def __str__(self):
		return str(self.id) + " - " + str(self.userName)
