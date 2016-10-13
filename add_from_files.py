import xlrd

from myapp.Item import *
import datetime, time
import myapp.Lib
import os


def get_true_false(s):
    if s == 'Y' or s == 'Yes' or s == 'YES':
        return True
    return False;


def process_file(file_name):
    print file_name
    # data = xlrd.open_workbook('06-15-eBiz.xlsx');
    data = xlrd.open_workbook(file_name);
    table = data.sheets()[0];
    nrow = table.nrows;
    for i in range(1, nrow):
        tmp = table.row_values(i);
        print tmp, type(tmp)
        dt = Lib.toStr(table.row_values(i)[0]);
        print type(dt)
        print dt, dt[0:2]
        a = Lib.toInt(dt[0:2]);
        b = Lib.toInt(dt[3:5]);
        c = Lib.toInt(dt[6:10]);

        date = datetime.date(c, a, b);
        number = Lib.toInt(table.row_values(i)[2])
        name = Lib.toStr(table.row_values(i)[1])
        buySingleCost = Lib.toFloat(table.row_values(i)[3])
        receivedNum = Lib.toInt(table.row_values(i)[5])
        sellSignlePrice = Lib.toInt(table.row_values(i)[6])
        receivedMoney = Lib.toInt(table.row_values(i)[8])
        otherCost = Lib.toFloat(table.row_values(i)[9])
        basicProfit = Lib.toFloat(table.row_values(i)[10])
        otherProfit = Lib.toFloat(table.row_values(i)[11])
        buyer = Lib.toStr(table.row_values(i)[13])
        buyPlace = Lib.toStr(table.row_values(i)[14])
        payCards = Lib.toStr(table.row_values(i)[16])
        ifDrop = get_true_false(table.row_values(i)[15])
        add_new_item(uID=0, date=date, name=name, number=number, buySingleCost=buySingleCost, \
                     receivedNum=receivedNum, sellSignlePrice=sellSignlePrice, receivedMoney=receivedMoney, \
                     otherCost=otherCost, basicProfit=basicProfit, otherProfit=otherProfit, buyer=buyer, \
                     buyPlace=buyPlace, payCards=payCards, ifDrop=ifDrop);


def process_all_files():
    info = os.getcwd();
    listfile = os.listdir(info);
    for i in range(len(listfile)):
        if listfile[i][-4:] == 'xlsx':
            process_file(listfile[i]);


if __name__ == '__main__':
    process_all_files();
