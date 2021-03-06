from myapp import app
import datetime
from peewee import *
from flask import (Flask, render_template, redirect,
    url_for, request,  make_response, flash)
import json
import Lib
from Tables import *

init_all_tables()

@app.route('/', methods=['GET'])
def home():
    all_items = PurchasedItem.all_items;
    sumItem = PurchasedItem.summary_item(all_items);
    return render_template("index.html",
                           date=Lib.get_current_date(),
                           all_items=all_items,
                           st_date=Lib.get_current_date(),
                           ed_date=Lib.get_current_date(),
                           sumItem=sumItem)


@app.route('/', methods=['POST'])
def selected_items(saves=""):
    data = {};
    # data is <select> date range
    data.update(dict(request.form.items()));
    st = data['start_date']
    ed = data['end_date']

    selected_items = PurchasedItem.get_items_time_range(st, ed);
    sumdic = PurchasedItem.summary_item(selected_items);
    return render_template("index.html", all_items=selected_items, sumItem=sumdic);


@app.route('/search_by_keyword', methods=['POST'])
def search_by_keyword():
    data = {};
    data.update(dict(request.form.items()));
    for x in data.items():
        print(x);
    keyword = data['keyword'].strip().lower();
    all_items = PurchasedItem.PurchasedItem.select();
    sumdic = PurchasedItem.summary_item(all_items);
    if (keyword != ""):
        all_items = PurchasedItem.get_items_by_keyword(keyword);
        sumdic = PurchasedItem.summary_item(all_items);
    return render_template("index.html", all_items=all_items, sumItem=sumdic);



@app.route('/recover', methods=['POST'])
def recover():
    data = {};
    data.update(dict(request.form.items()));
    print(data['uID']);
    uID = Lib.toInt(data['uID']);
    tmp = DeletedItem.DeletedItem.select().where(DeletedItem.DeletedItem.uID == uID);
    for x in tmp:
        PurchasedItem.copy_a_deleted_item(x);
        x.delete_instance();
    PurchasedItem.update_all_items();
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;


@app.route('/add_item')
def add_item():
    return render_template("add_item.html", all_items=PurchasedItem.all_items);

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'));
    except TypeError:
        data = {};
    return data;

@app.route('/save_new_item', methods=['POST'])
def save_new_item():
    data = {};
    data.update(dict(request.form.items()));
    PurchasedItem.add_new_item(name=data['name'], number=Lib.toInt(data['num']), \
                               buySingleCost=Lib.toFloat(data['buySingleCost']), \
                               sellSinglePrice=Lib.toFloat(data['sellSinglePrice']), \
                               otherCost=Lib.toFloat(data['otherCost']), \
                               otherProfit=Lib.toFloat(data['otherProfit']), \
                               buyer=data['buyer'], buyPlace=data['buyPlace'], \
                               payCards=data['payCards'], itemLocation=data['itemLocation'],
                               ifRegister=Lib.toBoolean(data['ifRegister']), remark=data['remark']);
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = {};
    data.update(dict(request.form.items()));
    PurchasedItem.delete_item_by_ID(Lib.toInt(data['delete']));
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;



@app.route('/show_deleted_item')
def show_deleted_item():
    deleted_items = DeletedItem.all_deleted_items;
    return render_template("deletedItems.html", all_items=deleted_items);



@app.route('/jump_revise_item', methods=['POST'])
def jump_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    response = make_response(redirect(url_for('revise_item', uID=data['revise'])));
    # response.set_cookie('character', json.dumps(data));
    return response;

@app.route('/revise_item/<int:uID>')
@app.route('/revise_item')
def revise_item(uID):
    item = PurchasedItem.get_item_by_ID(uID);
    ######################################testing#######
    # item.print_item()
    return render_template("revise_item.html", item=item);

@app.route('/save_revise_item', methods=['POST'])
def save_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    uID = Lib.toInt(data['uID']);
    for x in PurchasedItem.all_items:
        if x.uID == uID:
            x.name = data['name'];
            x.date = Lib.str_to_date(data['date']);
            x.number = Lib.toInt(data['num']);
            x.buySingleCost = Lib.toDecimal(Lib.toFloat(data['buySingleCost']));
            x.receivedNum = Lib.toInt(data['receivedNum']);
            x.sellSinglePrice = Lib.toDecimal(Lib.toFloat(data['sellSinglePrice']));
            x.receivedMoney = Lib.toDecimal(Lib.toFloat(data['receivedMoney']));
            x.otherCost = Lib.toDecimal(Lib.toFloat(data['otherCost']));
            x.otherProfit = Lib.toDecimal(Lib.toFloat(data['otherProfit']));
            x.buyer = data['buyer'];
            x.ifDrop = data['ifDrop'];
            x.buyPlace = data['buyPlace'];
            x.payCards = data['payCards'];
            x.itemLocation = data['itemLocation'];
            x.ifRegister = Lib.toBoolean(data['ifRegister']);
            x.remark = data['remark'];
            PurchasedItem.update_cost_and_profit(x);
            x.save();
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;
