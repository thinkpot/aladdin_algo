from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone_number(value):
    import re
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')  # Customize this regex as needed for your phone number format
    if not phone_regex.match(value):
        raise ValidationError(
            _('Invalid phone number format.'),
            code='invalid_phone_number'
        )
