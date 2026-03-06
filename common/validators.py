from datetime import datetime
from rest_framework.exceptions import ValidationError

def validator_birthdate(request):
    token=request.auth
    if not token or not token.get("birthdate"):
        raise ValidationError ("Enter yout date of birth to create a product")
    birthdate_str=token.get("birthdate")
    birthdate=datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    today=datetime.today().date()
    age=(today-birthdate).days // 365
    
    if age < 18:
        raise ValidationError ("You must be 18 y.o. to create product")