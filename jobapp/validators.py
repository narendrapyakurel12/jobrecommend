from django.core.exceptions import ValidationError


def validate_file(value):
    value = str(value)

    if value.endswith(".pdf") != True and value.endswith('.docs') != True and value.endswith(".docx") != True:
        raise ValidationError('only pdf and word documents can be uploaded')
    else:
        return value
