from flask import (request, render_template, redirect,
    url_for, request,  make_response, flash, Response, jsonify)
import json
from Tables import *
from User import *
from flask_cors import CORS, cross_origin
from playhouse.shortcuts import model_to_dict, dict_to_model

init_all_tables()
CORS(app)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            flash("You Had Already Signed In")
            return redirect(url_for('home'))
        return render_template('login.html', error=error)

    email = request.form.get('email', '')
    try:
        currentUser = User.get(User.email == email)
        if request.form['password'] == currentUser.password:
            user = User()
            user.id = email
            flask_login.login_user(user);
            flash("You were successfully logged in")
            return redirect(url_for('home'))
        error = "bad credencials"
        return render_template("login.html", error=error)
    except User.DoesNotExist:
        error = "User not Exists"
        return render_template("login.html", error=error)


# callback for login failures
@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauthorized.html')


@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user();
    return "You Have Been Successfully Logged Out"


# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     current_user_id = flask_login.current_user.id
#     refresh_all_tables(current_user_id)
#     # return 'Logged in as: ' + str(flask_login.current_user.username)
#     return redirect(url_for('home'))


@app.route('/', methods=['GET'])
@flask_login.login_required
def home():
    current_user_id = flask_login.current_user.id
    refresh_all_tables(current_user_id)
    all_items = PurchasedItem.all_items;
    sumItem = PurchasedItem.summary_item(all_items);
    return render_template("index.html",
                           date=Lib.get_current_date(),
                           all_items=all_items,
                           st_date=Lib.get_current_date(),
                           ed_date=Lib.get_current_date(),
                           sumItem=sumItem)


@app.route('/', methods=['POST'])
@flask_login.login_required
def selected_items(saves=""):
    data = {};
    # data is <select> date range
    data.update(dict(request.form.items()));
    st = data['start_date']
    ed = data['end_date']
    cur_user = flask_login.current_user.id
    selected_items = PurchasedItem.get_items_time_range(cur_user, st, ed)
    sumdic = PurchasedItem.summary_item(selected_items);
    return render_template("index.html", all_items=selected_items, sumItem=sumdic);



@app.route('/json', methods=["GET"])
def getItemsInJson():
    print "Enter /JSON"
    sidx = request.args.get('sidx')
    sord = request.args.get('sord')


    allItems = PurchasedItem.all_items
    jsonData = {}
    allItemsInJson = []
    totalRecords = len(allItems)
    try:
        print request.args
        rows = Lib.toInt(request.args.get('rows'))
        page = Lib.toInt(request.args.get('page'))

        jsonData["page"] = page
        # jsonData['total'] = (totalRecords+rows)/rows
    except NameError as error:
        print "nameError: " + error

    jsonData["records"] = totalRecords

    for item in allItems:
        temp = model_to_dict(item, recurse=False)
        newstr = str(temp["date"])
        temp["date"] = newstr
        allItemsInJson.append(temp)

    jsonData["data"] = allItemsInJson
    print jsonData
    return jsonify(**jsonData)

@app.route('/showall', methods=['GET'])
@flask_login.login_required
def showall():
    return render_template("showall.html")


@app.route('/search_by_keyword', methods=['POST'])
@flask_login.login_required
def search_by_keyword():
    cur_user = flask_login.current_user.id
    data = {};
    data.update(dict(request.form.items()));
    for x in data.items():
        print(x);
    keyword = data['keyword'].strip().lower();
    all_items = PurchasedItem.PurchasedItem.select().where(cur_user == PurchasedItem.PurchasedItem.user);
    sumdic = PurchasedItem.summary_item(all_items);
    if (keyword != ""):
        all_items = PurchasedItem.get_items_by_keyword(keyword);
        sumdic = PurchasedItem.summary_item(all_items);
    return render_template("index.html", all_items=all_items, sumItem=sumdic);


@app.route('/recover', methods=['POST'])
@flask_login.login_required
def recover():
    data = {};
    data.update(dict(request.form.items()));
    print(data['uID']);
    uID = Lib.toInt(data['uID']);
    tmp = DeletedItem.DeletedItem.select().where(DeletedItem.DeletedItem.uID == uID);
    for x in tmp:
        PurchasedItem.copy_a_deleted_item(x);
        x.delete_instance();
    PurchasedItem.update_all_items(flask_login.current_user.id);
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;


@app.route('/add_item')
@flask_login.login_required
def add_item():
    return render_template("add_item.html")


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'));
    except TypeError:
        data = {};
    return data;


@app.route('/save_new_item', methods=['POST'])
@flask_login.login_required
def save_new_item():
    curUser = flask_login.current_user.id
    data = {};
    data.update(dict(request.form.items()));
    PurchasedItem.add_new_item(user=curUser, name=data['name'], number=Lib.toInt(data['num']), \
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
@flask_login.login_required
def delete_item():
    data = {};
    data.update(dict(request.form.items()));
    PurchasedItem.delete_item_by_ID(Lib.toInt(data['delete']));
    response = make_response(redirect(url_for('home')));
    # response.set_cookie('character', json.dumps(data));
    return response;



@app.route('/show_deleted_item')
@flask_login.login_required
def show_deleted_item():
    deleted_items = DeletedItem.all_deleted_items;
    return render_template("deletedItems.html", all_items=deleted_items);


@app.route('/jump_revise_item', methods=['POST'])
@flask_login.login_required
def jump_revise_item():
    data = {};
    data.update(dict(request.form.items()));
    response = make_response(redirect(url_for('revise_item', uID=data['revise'])));
    # response.set_cookie('character', json.dumps(data));
    return response;


@app.route('/revise_item/<int:uID>')
@app.route('/revise_item')
@flask_login.login_required
def revise_item(uID):
    item = PurchasedItem.get_item_by_ID(uID);
    ######################################testing#######
    # item.print_item()
    return render_template("revise_item.html", item=item);


@app.route('/save_revise_item', methods=['POST'])
@flask_login.login_required
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
