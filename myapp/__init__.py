from flask import Flask


app = Flask(__name__)
# app.config.from_object("myappconfig")


import myapp.View, myapp.PurchasedItem, myapp.DeletedItem, myapp.User