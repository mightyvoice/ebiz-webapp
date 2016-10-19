#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from playhouse.migrate import *

# db = SqliteDatabase('test.db');
##############schema migrations############
# peewee’s migrations do not handle introspection and database “versioning”
# Rather, peewee provides a number of helper functions for generating and
#     running schema-altering statements. This engine provides the basis
#     on which a more sophisticated tool could some day be built.

db = SqliteDatabase('all_purchased_items.db')
migrator = SqliteMigrator(db)

# Create your field instances. For non-null fields you must specify a
# default value.

# user_field = ForeignKeyField(User, related_name="purchasedItems")
itemLocation_field = TextField(null=True)
ifRegister_field = BooleanField(default=False, null=True)
remark_field = TextField(null=True)

# Run the migration, specifying the database table, field name and field.
# migrate(
    # migrator.add_column('PurchasedItem', 'user', user_field),
    # migrator.add_column('PurchasedItem', 'itemLocation', itemLocation_field),
    # migrator.add_column('PurchasedItem', 'ifRegister', ifRegister_field),
    # migrator.add_column('PurchasedItem', 'remark', remark_field),
    # migrator.drop_not_null('PurchasedItem', 'ifRegister')

    # migrator.add_column('DeletedItem', 'itemLocation', itemLocation_field),
    # migrator.add_column('DeletedItem', 'ifRegister', ifRegister_field),
    # migrator.add_column('DeletedItem', 'remark', remark_field),

# )