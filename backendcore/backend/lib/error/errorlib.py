import logging
from rest_framework import status

from lib import constants as const
from lib.apiresponse import ApiResponse
from lib.error.errortype import ErrorType
from lib.error import errorutil, errormessage
from lib.error.exceptionlogger import logException
from lib.validationresponse import ValidationResponse

logger = logging.getLogger(__name__)

def getSingleFormatedError(errorResponse):
	errorMessage = None
	if const.ERROR_PROPERTY in errorResponse.response:
		errorMessage = errorResponse.response[const.ERROR_PROPERTY]
	elif const.ERROR_MESSAGE_PROPERTY in errorResponse.response:
		errorMessage = errorResponse.response[const.ERROR_MESSAGE_PROPERTY]
	return ApiResponse(
		errorutil.getSingleErrorFormat(errorMessage), errorResponse.status
	)

def get400Error(errorMsg, isApiResponse=False):
	return errorutil.getSingleErrorResponse(
		errorMsg, status.HTTP_400_BAD_REQUEST, isApiResponse
	)

def get401Error(errorMsg, isApiResponse=False):
	return errorutil.getSingleErrorResponse(
		errorMsg, status.HTTP_401_UNAUTHORIZED, isApiResponse
	)

def get403Error(errorMsg, isApiResponse=False):
	return errorutil.getSingleErrorResponse(
		errorMsg, status.HTTP_403_FORBIDDEN, isApiResponse
	)

def get404Error(errorMsg, isApiResponse=False):
	return errorutil.getSingleErrorResponse(
		errorMsg, status.HTTP_404_NOT_FOUND, isApiResponse
	)

def get409Error(errorMsg, isApiResponse=False):
	return errorutil.getSingleErrorResponse(
		errorMsg, status.HTTP_409_CONFLICT, isApiResponse
	)

def get500Error(exception=None, errorMsg=None, isApiResponse=False):
	errorMessage = errormessage.INTERNAL_SERVER_ERROR
	if errorMsg:
		errorMessage = errorMsg
	logException(logger, exception, errorMessage)
	return errorutil.getSingleErrorResponse(
		errorMessage, status.HTTP_500_INTERNAL_SERVER_ERROR, isApiResponse
	)

def getFieldErrorFromResposne(fieldName, response, isApiResponse=False):
	response = {
		const.ERROR_TYPE_PROPERTY: ErrorType.FIELD_ERROR,
		const.FIELD_PROPERTY: {fieldName: [response['errorMessage']]}
	}
	if isApiResponse:
		return response
	return ValidationResponse(False, response, status.HTTP_400_BAD_REQUEST)

def getFieldErrorApiResponse(fieldName, errorMessage, isApiResponse=False):
	response = {
		const.ERROR_TYPE_PROPERTY: ErrorType.FIELD_ERROR,
		const.FIELD_PROPERTY: {fieldName: [errorMessage]}
	}
	if isApiResponse:
		return response
	return ValidationResponse(False, response, status.HTTP_400_BAD_REQUEST)

