import re

def hasMixCase(password):
	return bool(re.search("([a-z].*[A-Z])|([A-Z].*[a-z])", password))

def hasNumber(password):
	return bool(re.search("[0-9]", password))

def hasSpecialCharacter(password):
	return bool(re.search("[^a-zA-Z0-9\s]", password))

def isStrongPassword(password):
	return (
		hasMixCase(password) and
		hasNumber(password) and
		hasSpecialCharacter(password)
	)
