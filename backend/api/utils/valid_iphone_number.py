import re

def is_valid_phone_number(phone_number):
    p = re.compile(r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$')
    s = re.search(p,phone_number)

    return bool(s)