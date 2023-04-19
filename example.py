
def authenticate(func):
    def wrapper():
        userids = [1, 2]
        if 10 in userids:
            func()
        else:
            print("Invalid")
    return wrapper

@authenticate
def login():
    print(f"Welcome {1}")

@authenticate
def signup():
    print(f"Registration success")

import os
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper():
        token = os.environ.get('TOKEN')
        if token:
            func()
        else:
            print("Missing token")
    return wrapper

@login_required
def get_profile():
    print({"name":"Hadiza Kano", "email":"so@gmail.com"})

@login_required
def get_friends():
    print(["Hadiza Kano", "Mardiya Salis"])

get_profile()
get_friends()

print(get_friends.__name__)

