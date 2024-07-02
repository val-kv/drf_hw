from rest_framework.serializers import ValidationError


def validate_materials_link(value):
    link = value
    if not link.startswith('https://youtube.com'):
        raise ValidationError('Link must be "https://youtube.com"')
    return link
