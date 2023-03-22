from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from lib.error import errormessage

class NonNegativeDecimalForm(forms.DecimalField):
	def validate(self, value):
		super().validate(value)
		if value < 0:
			raise ValidationError(errormessage.VALUE_MUST_BE_NON_NEGATIVE_ERROR)

class NonNegativeDecimalField(models.DecimalField):
	def get_db_prep_save(self, value, connection):
		value = super().get_db_prep_value(value, connection)
		if value < 0.00:
			raise ValueError(errormessage.VALUE_MUST_BE_NON_NEGATIVE_ERROR)
		return value

	def formfield(self, **kwargs):
		defaults = {
			'form_class': NonNegativeDecimalForm,
		}
		defaults.update(kwargs)
		return super().formfield(**defaults)
