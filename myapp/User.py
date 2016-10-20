import Lib
from MyDatabase import *

class User(Model):
    username = CharField(unique=True, max_length=120)
    email = CharField(max_length=50)
    password = CharField(max_length=50)

    class Meta:
        database = db

    def print_item(self):
        info = dict()
        info['username'] = self.username
        info['email'] = self.email
        info['password'] = self.password
        print(info.items())

def addNewUser(username="", email="", password=""):
    new_user = User(username=username, email=email, password=password)
    new_user.save()
    new_user.print_item()
    return new_user

def updateAllUsers():
    all_users = User.select()
    return all_users

