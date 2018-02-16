from django.core.exceptions import ValidationError

CATEGORIES = ["Italian", "Pizza", "Pub", 'Elit']

def validate_category(value):
	if value:
	    if not value in CATEGORIES and not value.capitalize() in CATEGORIES:
	        raise ValidationError(
	            f"{value} is not a valid category!"
	        )