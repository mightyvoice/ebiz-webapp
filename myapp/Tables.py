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
    # drop_all_tables();
    PurchasedItem.update_all_items();
    print "Item表格共有行数：" + str(len(PurchasedItem.all_items));
    # addDefaultUser()
    # q = PurchasedItem.PurchasedItem.update(buyer="4k").where(PurchasedItem.PurchasedItem.buyer == "李旭");
    # q.execute();

    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();


