#Simple-Ebiz-Webapp

##technoleges
* peewee(ORM)
* Flask
* Sqlite

## Main Function
* user log in & log out
* show all PurchasedItem / DeletedItem 
* Add, Revise, Delete PurchasedItem
* Add, Revise, Delete DeletedItem
* Add, Revise, Delete Card
* Filter By
	1. keywords
	2. buyer
	3. time span
	4. PaidCard
	5. ReceivedMoney

### Models
* PurchasedItem
* DeletedItem
	1. uID
	2. user(foreign key)
	2. date
	1. number
	1. name
	1. buySingleCost
	1. buyTotalCost
	1. receivedNum
	1. sellSignlePrice 
	1. sellTotalPrice 
	1. receivedMoney 
	1. otherCost 
	1. basicProfit 
	1. otherProfit 
	1. totalProfit 
	1. buyer
	1. buyPlace 
	1. payCards=
	1. ifDrop 
	2. itemLocation(need to add)
	3. ifRegister(need to add)
	4. remark
* Card
	1. bankName
	2. cardName
	3. billingDay
	4. dueDay
	3. creditLimit
	5. currentBalance
	6. remainingBalance
* User(next step)
	1. username-unique
	2. email-
	3. password



