import Lib
from MyDatabase import *

class User(Model):
    username = CharField(unique=True, max_length=120)
    email = TextField(max_length=50)
    password = CharField(max_length=50, min_length=8)

    class Meta:
        database = db

    def print_item(self):
        info = dict()
        info['username'] = self.username
        info['email'] = self.email
        info['password'] = self.password
        print(info.items())

if __name__ == '__main__':
    username = 'admin'
    email = 'ross917@gmail.com'
    password = 'a1234567'
    new_user = User(username=username, email=email, password=password)
    new_user.save()
    new_user.print_item()

