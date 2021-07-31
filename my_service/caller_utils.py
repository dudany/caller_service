from my_service.data_helper import DatabaseAccess

DEFAULT_VR = {"vendor": 150, "email_signature": 120, "address_book": 100, "community": 50, "scarping": 20,
              DatabaseAccess.BAD_SOURCE: float("-inf")}


class BaseInputError(Exception):
    def __init__(self, phone_number):
        self.phone_number = phone_number


class NameNotFoundError(BaseInputError):
    def __str__(self):
        return f"Not found a name matching this phone number: {self.phone_number}"


class BadSourceException(BaseInputError):
    def __str__(self):
        return f"This phone number associated with bad source: {self.phone_number}"


class BadPhoneNumberInput(BaseInputError):
    def __str__(self):
        return f"Bad phone number input: {self.phone_number} , use digits and \'-\' only "


def raise_on_bad_input(phone_number):
    # validating input is in the format of "123-123-1234" (contains only numbers and '-')
    for c in phone_number:
        if not (c.isdigit() or c == "-"):
            raise BadPhoneNumberInput(phone_number)
