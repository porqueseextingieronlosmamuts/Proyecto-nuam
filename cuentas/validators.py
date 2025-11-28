import re
from django.core.exceptions import ValidationError

def validate_password(value):
    # Expresión regular para la contraseña:
    # Al menos 8 caracteres, al menos una minúscula, una mayúscula, un número y un carácter especial
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\d]).{8,16}$'
    
    if not re.match(regex, value):
        raise ValidationError(
            'La contraseña debe tener entre 8 y 16 caracteres, incluir al menos una letra minúscula, una mayúscula, un número y un carácter especial.'
        )
