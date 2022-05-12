import re



class Validator():
    """Use this class to validate [email, password, name, etc.]"""
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email method that confirms if this valid email or not"""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return email if(re.fullmatch(regex, email)) else None

    @staticmethod
    def validate_string(string: str) -> bool:
        """Validate string method that confirms if this valid string or not"""
        regex = re.compile('[@!#$%^&*()<>?/\|}{-~: "]')
        return True if (regex.search(string) == None) else False