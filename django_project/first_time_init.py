#!/usr/bin/python

import os

from settings import (
    _secrets_file,
)

def create_secret_if_needed():
    if not os.path.exists(_secrets_file) or os.path.getsize(_secrets_file) == 0:
        with open(_secrets_file, "w") as f:
            # taken from django/core/management/commands/startproject.py
            from django.utils.crypto import get_random_string
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            f.write(get_random_string(50, chars))
        print("secret '%s' created succesfully" % _secrets_file)
    else:
        print("secret '%s' already exists" % _secrets_file)

if __name__ == "__main__":
    create_secret_if_needed()
