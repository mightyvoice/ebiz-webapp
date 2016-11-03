import datetime
from peewee import *
import Lib
from MyDatabase import *
import DeletedItem
from User import *

all_items = [];
item_list = [];

class PurchasedItem(Model):
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
    user = ForeignKeyField(User, related_name="purchasedItems", null=False)


    class Meta:
        database = db;
        order_by = ('-date',);

    def print_item(self):
        info = dict()
        info['uID'] = self.uID
        info['date'] = self.date
        info['number'] = self.number
        info['name'] = self.name
        info['buySingleCost'] = self.buySingleCost
        info['buyTotalCost'] = self.buyTotalCost
        info['receivedNum'] = self.receivedNum
        info['sellSinglePrice'] = self.sellSinglePrice
        info['sellTotalPrice'] = self.sellTotalPrice
        info['receivedMoney'] = self.receivedMoney
        info['otherCost'] = self.otherCost
        info['basicProfit'] = self.basicProfit
        print(info.items())


def update_all_items(user_id):
    global all_items;
    all_items = PurchasedItem.select().where(PurchasedItem.user == user_id);
    DeletedItem.all_deleted_items = DeletedItem.DeletedItem.select().where(DeletedItem.DeletedItem.user == user_id)


def update_cost_and_profit(_item):
    _item.buyTotalCost = Lib.toDecimal(_item.buySingleCost * _item.number);
    _item.sellTotalPrice = Lib.toDecimal(_item.sellSinglePrice * _item.number);
    _item.basicProfit = Lib.toDecimal(_item.sellTotalPrice - _item.buyTotalCost);
    _item.totalProfit = Lib.toDecimal(_item.basicProfit + _item.otherProfit - _item.otherCost);

def add_new_item(user, uID=0, date=Lib.get_current_date(), name="", number=0,
                 buySingleCost=0, buyTotalCost=0,
                 receivedNum=0, sellSinglePrice=0, sellTotalPrice=0, receivedMoney=0,
                 otherCost=0, basicProfit=0, otherProfit=0, totalProfit=0, buyer="",
                 buyPlace="", payCards="", ifDrop=False, itemLocation="", ifRegister=False, remark=""):
    new_item = PurchasedItem(user=user, uID=uID, date=date, name=name, number=number, buySingleCost=Lib.toDecimal(buySingleCost), \
                             buyTotalCost = Lib.toDecimal(buyTotalCost), \
                             sellSinglePrice=Lib.toDecimal(sellSinglePrice), sellTotalPrice=sellTotalPrice, \
                             receivedMoney=Lib.toDecimal(receivedMoney), receivedNum=receivedNum, otherCost=Lib.toDecimal(otherCost), \
                             basicProfit=Lib.toDecimal(basicProfit), otherProfit=Lib.toDecimal(otherProfit), \
                             totalProfit=Lib.toDecimal(totalProfit), buyer=buyer, buyPlace=buyPlace, payCards=payCards, \
                             ifDrop=ifDrop, itemLocation=itemLocation, ifRegister=ifRegister, remark=remark);

    if new_item.uID == 0:
    	new_item.uID = Lib.get_unique_ID();
    update_cost_and_profit(new_item);
    new_item.save();
    update_all_items(user);

def get_items_time_range(userid, _start=datetime.date(1,1,1), _end=Lib.get_current_date()):
    entries = PurchasedItem.select().order_by(PurchasedItem.date);
    ans = entries.where(PurchasedItem.user == userid)
    ans = ans.where(PurchasedItem.date >= _start)
    ans = ans.where(PurchasedItem.date <= _end)
    return ans;


def get_item_by_ID(_ID):
    for x in PurchasedItem.select():
        if x.uID == _ID:
            return x;

def delete_item_by_ID(_id):
    entries = PurchasedItem.select().where(PurchasedItem.uID == _id);
    user_id = entries[0].user
    for entry in entries:
        add_deleted_item(entry.uID);
        entry.delete_instance();
    update_all_items(user_id);

def delete_all_saved_items():
    for x in PurchasedItem.select():
        x.delete_instance();

def add_deleted_item(_id):
    deleted_items = PurchasedItem.select().where(PurchasedItem.uID == _id);
    for newitem in deleted_items:
        new_deleted_item = DeletedItem.DeletedItem(user=newitem.user, uID=newitem.uID, date=newitem.date, name=newitem.name, \
                                                   number=newitem.number, buySingleCost=newitem.buySingleCost, buyTotalCost=newitem.buyTotalCost, \
                                                   sellSinglePrice=newitem.sellSinglePrice, sellTotalPrice=newitem.sellTotalPrice, \
                                                   receivedMoney=newitem.receivedMoney, receivedNum=newitem.receivedNum, otherCost=newitem.otherCost, \
                                                   basicProfit=newitem.basicProfit, otherProfit=newitem.otherProfit, \
                                                   totalProfit=newitem.totalProfit, buyer=newitem.buyer, buyPlace=newitem.buyPlace, payCards=newitem.payCards, \
                                                   ifDrop=newitem.ifDrop,itemLocation=newitem.itemLocation, ifRegister=newitem.ifRegister, remark=newitem.remark);
        update_cost_and_profit(new_deleted_item);
        new_deleted_item.save();

def copy_a_deleted_item(_deletedItem):
	'''return a PurchasedItem the same as the _deletedItem'''
	add_new_item(user=_deletedItem.user, uID=_deletedItem.uID, \
                 date=_deletedItem.date, number=_deletedItem.number, name=_deletedItem.name, \
                 buySingleCost=_deletedItem.buySingleCost, \
                 receivedNum=_deletedItem.receivedNum, \
                 sellSinglePrice=_deletedItem.sellSinglePrice, \
                 receivedMoney=_deletedItem.receivedMoney, \
                 otherCost=_deletedItem.otherCost, \
                 basicProfit=_deletedItem.basicProfit, \
                 otherProfit=_deletedItem.otherProfit, \
                 totalProfit=_deletedItem.totalProfit, \
                 buyer=_deletedItem.buyer, \
                 buyPlace=_deletedItem.buyPlace, \
                 payCards=_deletedItem.payCards, \
                 ifDrop=_deletedItem.ifDrop,
                 itemLocation=_deletedItem.itemLocation, \
                 ifRegister=_deletedItem.ifRegister, \
                 remark=_deletedItem.remark);

# -------------------------
#     items summary row
# --------------------------

def summary_item(_items):
    sumItem = {};
    sumItem['sumBuyTotalCost'] = 0;
    sumItem['sumSellTotalPrice'] = 0;
    sumItem['sumReceivedMoney'] = 0;
    sumItem['sumOtherCost'] = 0;
    sumItem['sumBasicProfit'] = 0;
    sumItem['sumOtherProfit'] = 0;
    sumItem['sumTotalProfit'] = 0;
    if (_items):
        for x in _items:
            sumItem['sumBuyTotalCost'] += x.buyTotalCost;
            sumItem['sumSellTotalPrice'] += x.sellTotalPrice;
            sumItem['sumOtherCost'] += x.otherCost;
            sumItem['sumBasicProfit'] += x.basicProfit;
            sumItem['sumOtherProfit'] += x.otherProfit;
            sumItem['sumTotalProfit'] += x.totalProfit;
            sumItem['sumReceivedMoney'] += x.receivedMoney;
    sumItem['sumBuyTotalCost'] = Lib.toDecimal(sumItem['sumBuyTotalCost']);
    sumItem['sumSellTotalPrice'] = Lib.toDecimal(sumItem['sumSellTotalPrice'] );
    sumItem['sumReceivedMoney'] = Lib.toDecimal(sumItem['sumReceivedMoney']);
    sumItem['sumOtherCost'] = Lib.toDecimal(sumItem['sumOtherCost']);
    sumItem['sumBasicProfit'] = Lib.toDecimal(sumItem['sumBasicProfit']);
    sumItem['sumOtherProfit'] = Lib.toDecimal(sumItem['sumOtherProfit']);
    sumItem['sumTotalProfit'] = Lib.toDecimal(sumItem['sumTotalProfit']);
    return sumItem;

def get_items_by_keyword(_keyword):
    del item_list[:];
    for x in all_items:
        itemstring = "";
        itemstring += x.name.strip().lower();
        itemstring += x.buyer.strip().lower();
        itemstring += x.buyPlace.strip().lower();
        itemstring += x.payCards.strip().lower();
        if _keyword in itemstring:
            item_list.append(x);
    return item_list;
    

