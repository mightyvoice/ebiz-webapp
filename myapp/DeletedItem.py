import datetime
from peewee import *
import Lib
from MyDatabase import *

all_deleted_items = [];

class DeletedItem(Model):
    uID = IntegerField(unique=True);
    date = DateField();
    number = IntegerField();
    name = TextField();
    buySingleCost = DoubleField();
    buyTotalCost = DoubleField();
    receivedNum = IntegerField();
    sellSinglePrice = DoubleField();
    sellTotalPrice = DoubleField();
    receivedMoney = DoubleField();
    otherCost = DoubleField();
    basicProfit = DoubleField();
    otherProfit = DoubleField();
    totalProfit = DoubleField();
    buyer = CharField(max_length=120);
    buyPlace = CharField(max_length=120);
    payCards = TextField();
    ifDrop = BooleanField();
    itemLocation = TextField()
    ifRegister = BooleanField();
    remark = TextField();

    class Meta:
        database = db


def delete_all_deleted_items():
    for x in DeletedItem.select():
        x.delete_instance();

