"""Conatines a generate_password function"""
import secrets
import string


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(20))
    return password
