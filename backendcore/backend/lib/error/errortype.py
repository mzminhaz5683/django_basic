from dataclasses import dataclass

@dataclass(frozen=True)
class ErrorType:
	SINGLE_ERROR = "SingleError"
	FIELD_ERROR = "FieldError"
	FORM_SET_ERROR = "FormSetError"
