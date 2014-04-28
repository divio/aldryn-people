# -*- coding: utf-8 -*-
from django.template.base import Library

from phonenumbers import parse, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException


register = Library()


@register.filter(is_safe=True)
def phoneformat(phone_number, phone_format='INTERNATIONAL'):
    try:
        parsed_number = parse(phone_number, None)
        format = getattr(PhoneNumberFormat, phone_format)
        return format_number(parsed_number, format)
    except NumberParseException:
        return phone_number
