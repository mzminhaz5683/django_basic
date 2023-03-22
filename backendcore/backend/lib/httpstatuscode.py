from dataclasses import dataclass

@dataclass(frozen=True)
class HttpStatusCode:
	CREATED = 201
	OK = 200
	BAD_REQUEST = 400
	INTERNAL_SERVER_ERROR = 500
	NOT_FOUND = 404
	METHOD_NOT_ALLOWED = 405
	FORBIDDEN = 403
	UNPROCESSABLE_ENTITY = 422
