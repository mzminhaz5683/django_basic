import typing
from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationResponse:
	isValid: bool
	response: typing.Any
	status: typing.Any = None
