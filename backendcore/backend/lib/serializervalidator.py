import os, re, copy
from decimal import Decimal
from datetime import datetime, timezone
from rest_framework import serializers

IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']
TIME_PROPERTIES = ['H', 'M', 'S', 'I']

def getSerializerError(errorMessage):
	raise serializers.ValidationError(errorMessage, code='invalid')

def getGeneralValidation(value):
	if not value or value == 'None' or value == 'null' or value == "":
		return None
	return value

def isTimePropertiesHandled(pattern):
	return any([timeProperty in pattern for timeProperty in TIME_PROPERTIES])

def getDateTimeValidation(value, pattern, shouldCheckFutureDate=False):
	# pattern can be: "%m%Y", "%d%m%Y", "%d%m%y"
	givenValue = copy.deepcopy(value)
	if not value or value == 'None' or value == 'null' or value == "":
		return None
	finalTime = timeNow = datetime.now(timezone.utc)
	cleanedValue = givenValue.replace('"', '').replace("'", "")
	try:
		givenTime = datetime.strptime(cleanedValue, pattern)
		if not isTimePropertiesHandled(pattern):
			finalTime = finalTime.replace(
				year=givenTime.year, month=givenTime.month, day=givenTime.day
			)
		else:
			finalTime = givenTime.replace(tzinfo=timezone.utc)
	except Exception as e:
		return getSerializerError(f'Invalid date format')
	if shouldCheckFutureDate and not (timeNow < finalTime):
		return getSerializerError('Must be a future date')
	return finalTime # return utc datetime object

def getImageValidation(file):
	if not file or file == 'None' or file == 'null' or file == "":
		return None
	extension = os.path.splitext(file.name)[1].replace(".", "")
	if extension.lower() not in IMAGE_EXTENSIONS:
		return getSerializerError(f'Invalid file type: {IMAGE_EXTENSIONS}')
	return file

def getAmountValidation(value, minAmount='0.01'):
	#Decimal comparation returns
	# 1 – if a > b
	# -1 – if a < b
	# 0 – if a = b
	#If value is greater than MIN_PURCHASE we get 1,
	#If value is equal to MIN_PURCHASE we get 0
	#therefore we ensure result of this comparison is less than 0
	#for negative case. NOTE we have to also convert Decimal obj to int
	givenValue = copy.deepcopy(value)
	if not value or value == 'None' or value == 'null' or value == "":
		givenValue = '0'
	if not re.match("^([0-9]+)(.[0-9]+)?$", str(givenValue)):
		return getSerializerError('Invalid amount')
	if int(Decimal(givenValue).compare(Decimal(minAmount))) < 0:
		return getSerializerError(f'Minimum amount is {minAmount}')
	return Decimal(givenValue)
