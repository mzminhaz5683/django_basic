import json
import logging
from rest_framework import status
from django.shortcuts import render

from lib import constants as const
from lib.error import errormessage
from lib.error.errortype import ErrorType
from lib.httpstatuscode import HttpStatusCode
from lib.validationresponse import ValidationResponse
from lib.apiresponse import ApiResponse
from lib.error.exceptionlogger import logException

logger = logging.getLogger(__name__)

def getFormSetErrorResponse(formSetError):
	response = {
		const.ERROR_PROPERTY: {
			const.ERROR_TYPE_PROPERTY: ErrorType.FORM_SET_ERROR,
			const.FORM_SET_ERRORS_PROPERTY: formSetError
		}
	}
	return ValidationResponse(False, response, HttpStatusCode.BAD_REQUEST)

def getSingleErrorFormat(errorMsg):
	return {const.ERROR_PROPERTY: {
		const.ERROR_TYPE_PROPERTY: ErrorType.SINGLE_ERROR,
		const.ERROR_MESSAGE_PROPERTY: errorMsg
	}}

def getSingleError(errorMsg, statusCode):
	response = getSingleErrorFormat(errorMsg)
	return ValidationResponse(False, response, statusCode)

def getInternalServerErrorResponse():
	errorResponse = getSingleError(
		errormessage.INTERNAL_SERVER_ERROR,
		HttpStatusCode.INTERNAL_SERVER_ERROR
	)
	return errorResponse.response, errorResponse.status

def getInvalidMethodErrorContext(requestMethod, role):
	return {
		const.ERROR_PROPERTY:
			requestMethod + errormessage.METHOD_NOT_ALLOWED_ERROR,
		const.ROLE_PROPERTY: role
	}

def getInvalidMethodErrorResponse(requestMethod):
	errorResponse = getSingleError(
		requestMethod + errormessage.METHOD_NOT_ALLOWED_ERROR,
		HttpStatusCode.METHOD_NOT_ALLOWED
	)
	return errorResponse.response, errorResponse.status

def getPermissionError(errorMsg):
	response = getSingleErrorFormat(errorMsg)
	return ValidationResponse(False, response, HttpStatusCode.FORBIDDEN)

def getTemplateError(errorMsg, existingResponse=None):
	response = {const.ERROR_PROPERTY: errorMsg}
	if existingResponse:
		response.update(existingResponse)
	return ValidationResponse(False, response, None)

def getError(errorType, errorMessage, statusCode, isApiResponse=False):
	errorResponse = {const.ERROR_TYPE_PROPERTY: errorType}
	if errorType == ErrorType.SINGLE_ERROR:
		errorResponse[const.ERROR_MESSAGE_PROPERTY] = errorMessage
	else:
		errorResponse[const.FIELD_PROPERTY] = errorMessage
	if isApiResponse:
		return ApiResponse(errorResponse, statusCode)
	else:
		return ValidationResponse(False, errorResponse, statusCode)

def getSerilizerError(errors):
	return getError(
		ErrorType.FIELD_ERROR, errors, status.HTTP_400_BAD_REQUEST, True
	)

def getSingleErrorResponse(errorMsg, statusCode, isApiResponse=False):
	return getError(ErrorType.SINGLE_ERROR, errorMsg, statusCode, isApiResponse)

def getJSONParseError(exception):
	logException(logger, exception, errormessage.INVALID_JSON_FORMAT_ERROR)
	return getSingleErrorResponse(
		errormessage.INVALID_JSON_FORMAT_ERROR,
		status.HTTP_400_BAD_REQUEST,
		True
	)

def renderToErrorWebView(request, errorMsg):
	context = {const.ERROR_PROPERTY: errorMsg}
	return render(request, 'error/errorview.html', context)

def getFieldErrorResponse(formErrors):
	response = {
		const.ERROR_PROPERTY:{const.ERROR_TYPE_PROPERTY: ErrorType.FIELD_ERROR}
	}
	errors = json.loads(formErrors.as_json())
	for field in errors:
		response[const.ERROR_PROPERTY][field] = \
			errors[field][0][const.MESSAGE_PROPERTY]
	return ValidationResponse(False, response, HttpStatusCode.BAD_REQUEST)
