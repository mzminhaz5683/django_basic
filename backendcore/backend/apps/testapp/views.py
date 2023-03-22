import logging
from django.http import JsonResponse

logger = logging.getLogger('django')

def log(request):
	response = {'Hello test'}
	print("log: for general cases. But won't work sometime, when using docker")
	logger.info('log: for success message')
	logger.warning('log: for warning message')
	logger.error('log: for error message')
	logger.critical('log: for super danger message')

	return JsonResponse(response, status=200)
