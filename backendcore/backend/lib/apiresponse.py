from dataclasses import dataclass

@dataclass(frozen=True)
class ApiResponse:
	response: dict
	status: int
