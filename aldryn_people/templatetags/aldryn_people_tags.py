# -*- coding: utf-8 -*-
from django.template.base import Library

from phonenumbers.phonenumberutil import NumberParseException

from phonenumber_field.phonenumber import PhoneNumber


register = Library()


@register.filter(is_safe=True)
def phoneformat(phone_number, phone_format='international'):
    if not isinstance(phone_number, PhoneNumber):
        try:
            phone_number = PhoneNumber.from_string(phone_number)
        except NumberParseException:
            return phone_number
    return getattr(phone_number, 'as_%s' % phone_format, phone_number)
