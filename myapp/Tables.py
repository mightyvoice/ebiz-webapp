#!/usr/bin/env python
# -*- coding: utf-8 -*-

import DeletedItem
import PurchasedItem
import User
from MyDatabase import *

# ---------------------
# ---for test only use with caution---
# ---------------------
def drop_all_tables():
    db.drop_tables([PurchasedItem.PurchasedItem, DeletedItem.DeletedItem]);


def addDefaultUser():
    username = 'admin'
    email = 'ross917@gmail.com'
    password = 'a1234567'
    User.addNewUser(username=username, email=email, password=password)

def init_all_tables():
    db.connect();
    db.create_tables([PurchasedItem.PurchasedItem, DeletedItem.DeletedItem, User.User], safe=True);
    print "init tables"
    # drop_all_tables();
    # addDefaultUser()
    # q = PurchasedItem.PurchasedItem.update(buyer="4k").where(PurchasedItem.PurchasedItem.buyer == "李旭");
    # q.execute();
    # DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();

    # PurchasedItem.update_all_items();
    # print "PurchasedItem Table Rows: " + str(len(PurchasedItem.all_items))
    # print "DeletedItem Table Rows: " + str(len(DeletedItem.all_deleted_items))


def refresh_all_tables(user_id):
    PurchasedItem.update_all_items(user_id);
    print "PurchasedItem Table Rows: " + str(len(PurchasedItem.all_items))
    print "DeletedItem Table Rows: " + str(len(DeletedItem.all_deleted_items))