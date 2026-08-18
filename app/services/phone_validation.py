import phonenumbers

def is_valid_phone(number: str, country_code: str = None) -> bool:
    try:
        parsed = phonenumbers.parse(number, country_code)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False

def format_phone(number: str, country_code: str = None) -> str:
    parsed = phonenumbers.parse(number, country_code)
    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)