from playhouse.shortcuts import model_to_dict, dict_to_model
from Tables import *

def getItemsInJson():
    allItems = PurchasedItem.all_items;
    allItemsInJson = [];
    for item in allItems:
        temp = model_to_dict(item, recurse=False)
        newstr = str(temp['date'])
        temp['date'] = newstr
        # try:
        #     tmpDatetime = temp['date']
        #     print tempDatetime
        #     strDatetime = json.dumps(tmpDatetime, default=json_serial)
        #     temp['date'] = strDatetime[:10]
        #     print strDatetime
        #     print temp['date']
        # except:
        #     TypeError('Update not success')
        allItemsInJson.append(temp)
        print allItemsInJson

getItemsInJson()