def logException(logger, exception, errorMessage):
	if exception:
		logger.error(exception, exc_info=True)
	logger.error(errorMessage)
