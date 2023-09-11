from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def max_image_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_("Fayl çox böyükdür. Ölçü 5 MiB-dən çox olmamalıdır."))
