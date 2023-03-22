import logging
from django.http import JsonResponse

logger = logging.getLogger('django')

def log(request):
	response = {
		'For postman request calls, check': 'backend/apps/testapi/urls.py',
		 'To change the server ip' : 'update backendcore/runlocal.sh file target ip. (Default: 0.0.0.0:8000)'
	}

	print("log: for general cases. But won't work sometime, when using docker")
	logger.info('log: for success message')
	logger.warning('log: for warning message')
	logger.error('log: for error message')
	logger.critical('log: for super danger message')

	return JsonResponse(response, status=200)
