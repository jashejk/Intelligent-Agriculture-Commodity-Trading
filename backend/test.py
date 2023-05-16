import re


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_input(**kwargs):
    for arg_name, arg_value in kwargs.items():
        if arg_value is None:
            return False
    return True


print(is_valid_input("ss"))