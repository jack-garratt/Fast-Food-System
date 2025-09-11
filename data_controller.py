import sqlite3
import os
import random
import sys

if __name__ == "__main__":
    sys.exit("This should not be run directly, please use launcher.py")

def test(): #Ensure that the user is running the whole project. This is also called by every program at th start.
    if not os.path.exists("orders.db"):
        raise FileNotFoundError("orders.db not found. Run launcher.py to create it.")

def create_db():  #Setup all databases and tables required at once
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    sqlCommand = """
    CREATE TABLE IF NOT EXISTS tblItems (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NTO NULL
    )"""
    cursor.execute(sqlCommand)

    sqlCommand = """ 
    CREATE TABLE IF NOT EXISTS tblOrderItems (
    orderID INTEGER  NOT NULL,
    item TEXT NOT NULL,
    quantity TEXT NOT NULL,
    status TEXT NOT NULL
    )"""
    cursor.execute(sqlCommand)

    sqlCommand = """
    CREATE TABLE IF NOT EXISTS tblCompleted (
    orderID INTEGER  NOT NULL PRIMARY KEY
    )"""
    cursor.execute(sqlCommand)    

    cursor.execute("Select * from tblItems")
    if cursor.fetchall() == []: #In future updates this may be able to be managed by a seperate manager dashboard.
        defaultItems = [[48392175,"Classic Beef Burger","A juicy beef patty grilled to perfection.",4.99],
                        [90317462,"Spicy Chicken Wrap","Crispy spicy chicken strips wrapped in a soft tortilla.",3.49],
                        [17284039,"Loaded Fries"," Golden fries topped with melted cheese and smoked bacon bits.",2.99],
                        [61749382,"Veggie Deluxe Burger","A crispy plant-based patty served with fresh greens",4.49],
                        [53810476,"BBQ Chicken Wings (6pc)","Tender chicken wings coated in a BBQ sauce.",5.29],
                        [74938210,"Fish Fillet Sandwich","A crispy fish fillet topped with tartar sauce and lettuce",3.99],
                        [32849176,"Cheesy Nacho Bites (8pc)","Crunchy nacho-coated bites filled with melted cheese.",2.59],
                        [18476325,"Breakfast Muffin","A warm English muffin stacked with sausage, egg, and cheese.",2.99],
                        [90513284,"Chocolate Shake (Regular)","Thick chocolate milkshake with ice cream and whipped cream.",2.79],
                        [30284791,"Classic Chicken Nuggets (6pc)","Crispy chicken nuggets, seasoned and fried .",3.19],]
        for item in defaultItems:
            cursor.execute("INSERT INTO tblItems (id, name, description, price) VALUES (?,?,?,?)", item)
            conn.commit()

    

    conn.close()

def retreiveItems(): #This is for ordering.py so that it can see all items in the database without having to store the list localy.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute("Select * from tblItems")
    items = cursor.fetchall() 
    conn.close() 
    return items

def createOrder(order): #This creates an order ID and then adds the ID and the order to the database so that it can be made by fufillment.py
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 

    #Work out an ID
    id = random.randint(1000,9999)
    valid = False
    while valid == False:
        for item in retreiveItems():
            if item[0] == id:              #Prevents multiple order ID's from being the same
                valid = False
                id = random.randint(1000,9999)
        valid = True
                

    print(order)
    for item in order:
        finalItem = []   #Puts in item with ID in front
        finalItem.append(id)
        finalItem.append(item[0])
        finalItem.append(item[1])
        finalItem.append("received")
        cursor.execute("INSERT INTO tblOrderItems (orderID, item, quantity, status) VALUES (?,?,?,?)", finalItem)
        conn.commit()
    conn.close()


def fetch_orders(): #This is a very used module that allows any of the main screens to look up all active orders in an easy and readable form.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute("Select * from tblOrderItems")
    items = cursor.fetchall()  
    orders = []
    ids = []
    for item in items: #Creates a list of all order ID's
        if item[0] not in ids:
            ids.append(item[0])

    for id in ids: #create a list in the orders list where index 0 is the order ID
        orders.append([id])

    for count in range (len(ids)): #Add all items to the induvidual order list in the orders array
        for item in items:
            if item[0] == ids[count]:
                orders[count].append([item[1],item[2],item[3]])
    conn.close()
    return(orders)

def update_status(orderid, itemid, newstatus): #This is used when an item is marked as made by the fufillment window so that it is updated in the datbase
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute("UPDATE tblOrderItems SET status = ? WHERE orderID == ? AND item == ?",(newstatus,orderid,itemid)) 
    conn.commit()
    conn.close()

def fetch_status(orderid, itemid): #This is used so that the fufillment window can recover from a system crash with the same data.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute("SELECT status FROM tblOrderItems WHERE orderID == ? AND item == ?",(orderid,itemid))
    result = cursor.fetchall()
    conn.close()
    return result

def get_name(itemid): #This is used so that the system is able to access the name of an item given only the items ID
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute(f"SELECT name FROM tblItems WHERE id = {itemid}")
    name = cursor.fetchall()
    conn.close()
    return name

def move_order_complete(orderid): #This is used when the kitchen send out an order so that it is removed from the active order database. And moved to ready to collect where less information is needed.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    try:
        cursor.execute(f"INSERT INTO tblCompleted (orderID) VALUES ({orderid})")
        cursor.execute(f"DELETE FROM tblOrderItems WHERE orderID = {orderid}")
    except:
        print("UNABLE TO REMOVE ID THAT DOES NOT EXIST!")
    conn.commit()
    conn.close()

def fetch_kitchen_ids(): #This returns a list of all ids that are in the kitchen still being cooked. This is used by the progress window.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()  
    cursor.execute("Select orderID from tblOrderItems")
    raw_ids = cursor.fetchall() 
    conn.close() 
    ids = []
    for id in raw_ids:
        if id not in ids:
            ids.append(id)
    return ids

def fetch_sent_ids(): #This retreives a list of all ID's that have been sent out by the kitchen but nto yet collected.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()  
    cursor.execute("Select * from tblCompleted")
    ids = cursor.fetchall()
    conn.close()
    return ids

def order_collected(orderID): # This removes orders from the database when they are collected. In an updated version this would move to a database to be analyzed by a manager.
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor() 
    cursor.execute(f"DELETE FROM tblCompleted WHERE orderID = {orderID}")
    conn.commit()
    conn.close()
