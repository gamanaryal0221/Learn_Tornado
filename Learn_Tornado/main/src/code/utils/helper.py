import re


def is_valid_email(input):    
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    # Using re.match() to check if the provided string matches the pattern
    if re.match(email_pattern, input):
        return True
    else:
        return False