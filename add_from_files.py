import xlrd

from myapp.Item import *
import datetime
import Lib
import os


def get_true_false(s):
    if s == 'Y' or s == 'Yes' or s == 'YES':
        return True
    return False;


def process_file(file_name):
    print "****************--------------**************"
    print file_name
    # data = xlrd.open_workbook('06-15-eBiz.xlsx');
    data = xlrd.open_workbook(file_name);
    try:
        table = data.sheets()[0];
    except:
        return "No sheets exists in file"
    numberOfRows = table.nrows;
    if numberOfRows <= 1:
        return "No records in file"
    for i in range(1, numberOfRows):
        entireRowInList = table.row_values(i);
        print entireRowInList, type(entireRowInList)

        dt = entireRowInList[0]
        print type(dt)
        print dt
        a = Lib.toInt(dt[0:2])
        b = Lib.toInt(dt[3:5])
        c = Lib.toInt(dt[6:10])

        date = datetime.date(c, a, b);

        number = Lib.toInt(entireRowInList[2])
        name = entireRowInList[1]
        print name
        print type(name)

        buySingleCost = Lib.toFloat(table.row_values(i)[3])
        receivedNum = Lib.toInt(table.row_values(i)[5])
        sellSignlePrice = Lib.toInt(table.row_values(i)[6])
        receivedMoney = Lib.toInt(table.row_values(i)[8])
        otherCost = Lib.toFloat(table.row_values(i)[9])
        basicProfit = Lib.toFloat(table.row_values(i)[10])
        otherProfit = Lib.toFloat(table.row_values(i)[11])
        buyer = table.row_values(i)[13]
        print buyer
        buyPlace = table.row_values(i)[14]
        print buyPlace
        payCards = table.row_values(i)[16]
        ifDrop = get_true_false(table.row_values(i)[15])
        add_new_item(uID=0, date=date, name=name, number=number, buySingleCost=buySingleCost, \
                     receivedNum=receivedNum, sellSignlePrice=sellSignlePrice, receivedMoney=receivedMoney, \
                     otherCost=otherCost, basicProfit=basicProfit, otherProfit=otherProfit, buyer=buyer, \
                     buyPlace=buyPlace, payCards=payCards, ifDrop=ifDrop)


def process_all_files():
    info = os.getcwd();
    listfile = os.listdir(info);
    for i in range(len(listfile)):
        if listfile[i][-4:] == 'xlsx':
            process_file(listfile[i]);


if __name__ == '__main__':
    process_all_files();
