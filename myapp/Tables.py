#!/usr/bin/env python
# -*- coding: utf-8 -*-

import DeletedItem
import PurchasedItem
from MyDatabase import *

# ---------------------
# ---for test only use with caution---
# ---------------------
def drop_all_tables():
    db.drop_tables([PurchasedItem.PurchasedItem, DeletedItem.DeletedItem]);


def init_all_tables():
    db.connect();
    db.create_tables([PurchasedItem.PurchasedItem, DeletedItem.DeletedItem], safe=True);
    # drop_all_tables();
    PurchasedItem.update_all_items();
    print "Item表格共有行数：" + str(len(PurchasedItem.all_items));
    
    # q = PurchasedItem.PurchasedItem.update(buyer="4k").where(PurchasedItem.PurchasedItem.buyer == "李旭");
    # q.execute();

    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();


