#!/usr/bin/env python
# -*- coding: utf-8 -*-

import DeletedItem
import Item
from MyDatabase import *

# ---------------------
# ---for test only use with caution---
# ---------------------
def drop_all_tables():
    db.drop_tables([Item.Item, DeletedItem.DeletedItem]);


def init_all_tables():
    db.connect();
    db.create_tables([Item.Item, DeletedItem.DeletedItem], safe=True);
    # drop_all_tables();
    Item.update_all_items();
    # Item.all_items = Item.Item.select();
    print "Item表格共有行数：" + str(len(Item.all_items));
    
    q = Item.Item.update(buyer="4k").where(Item.Item.buyer == "李旭");
    q.execute();

    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select();


