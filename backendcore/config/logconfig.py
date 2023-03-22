import sys

BYTES_PER_KILOBYTE = 1024
KILOBYTE_PER_MEGABYTE = 1024
LOG_HANDLER_NAME = "backendcore"
MAX_LOG_FILE_SIZE_IN_BYTES = 1024 * 1024 * 5 # 5MB

def getLogConfig(logDir, isDebug, osSeperator):
	logFileName = LOG_HANDLER_NAME + ".log"

	logConfig = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'standard': {
				'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
			},
		},
		'handlers': {
			LOG_HANDLER_NAME: {
				'level': 'DEBUG',
				'class': 'logging.handlers.RotatingFileHandler',
				'filename': logDir + osSeperator + logFileName,
				'maxBytes': MAX_LOG_FILE_SIZE_IN_BYTES,
				'formatter': 'standard',
			},
		},
		'loggers': {
			'': {
				'handlers': [LOG_HANDLER_NAME],
				'level': 'DEBUG',
				'propagate': True
			},
			'django.request': {
				'handlers': [LOG_HANDLER_NAME],
				'level': 'DEBUG',
				'propagate': False,
			}
		}
	}
	if isDebug:
		logConfig['handlers']['console'] = {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'stream': sys.stdout
		}
		logConfig['loggers']['']['handlers'].append('console')
		logConfig['loggers']['django.request']['handlers'].append('console')
	return logConfig
