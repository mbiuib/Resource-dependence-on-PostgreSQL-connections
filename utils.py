import string
from random import choice
import phonenumbers
from phonenumbers import PhoneNumberFormat, format_number, PhoneNumberType, national_significant_number
from faker import Faker


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def generate_number():
    country_code = Faker().country_code()

    sample_number_obj = phonenumbers.example_number_for_type(country_code, PhoneNumberType.MOBILE)
    national_number_length = len(national_significant_number(sample_number_obj))

    number_obj = phonenumbers.parse(str(Faker().random_number(national_number_length)), country_code)
    number = phonenumbers.format_number(number_obj, phonenumbers.PhoneNumberFormat.E164)
    return number


def clear_n(l: list[str]):
    for line in l:
        line = line.strip("\n")
