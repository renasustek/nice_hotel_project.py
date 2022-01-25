import sqlite3#imports sql into python
import re
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
import datetime
now = datetime.datetime.now().year

from appjar import gui

def create_database():#function that creates an empty database
 
    #creates the user table

    cur.execute("""CREATE TABLE IF NOT EXISTS user_table (
                user_id INTEGER PRIMARY KEY,
                d_name TEXT NOT NULL UNIQUE,
                d_password TEXT NOT NULL,
                email	TEXT NOT NULL UNIQUE
        );
    """)
    #creates the payment table
    cur.execute("""CREATE TABLE IF NOT EXISTS "payment_table" (
                "payment_id" INTEGER PRIMARY KEY,
                "card_number" INTEGER NOT NULL,
                "name_on_card" TEXT NOT NULL,
                "expiration_date" INTEGER NOT NULL,
                "cvv" INTEGER NOT NULL,
                "user_id" INTEGER NOT NULL,
                FOREIGN KEY("user_id") REFERENCES "user_table"
                );
    """)
    #creates the bookings table
    cur.execute("""CREATE TABLE IF NOT EXISTS "booking_table" (
                    "booking_id" INTEGER PRIMARY KEY,
                    "user_id" INTEGER NOT NULL,
                    "room_id" INTEGER NOT NULL,
                    "check_in" INTEGER NOT NULL,
                    "check_out"	INTEGER NOT NULL,
                    "number_of_adults"	INTEGER NOT NULL,
                    "number_of_children" INTEGER NOT NULL,
                    "breckfast"	INTEGER,
                    "lunch" INTEGER,
                    "dinner" INTEGER,
                    "wifi" INTEGER,
                    FOREIGN KEY("room_id") REFERENCES "booking_table",
                    FOREIGN KEY("user_id") REFERENCES "user_table"
    );
    """)
    # creates the rooms table
    cur.execute("""CREATE TABLE IF NOT EXISTS "rooms_table" (
                "rooms_id"	INTEGER PRIMARY KEY,
                "room_number"	INTEGER NOT NULL,
                PRIMARY KEY("rooms_id")
    );
    """)
    # creates review table
    cur.execute("""CREATE TABLE IF NOT EXISTS "review_table" (
                    "review_id" INTEGER NOT NULL,
                    "user_id" INTEGER NOT NULL UNIQUE,
                    "rating" INTEGER NOT NULL UNIQUE,
                    "user_review" TEXT NOT NULL UNIQUE,
                    PRIMARY KEY("review_id")
                    
);
    """)


def create_interface():


    #app.startSubWindow("LOGIN_MENU")
    app.startTabbedFrame("FIRST MENU")  ## CREATES A TABBED FRAME##

    app.startTab("main_menu_tab")  ## creates a main menu tab ##
    app.addLabel("l1", "MAIN MENU")
    app.stopTab()

    app.startTab("login_tab")  ## creates a login tab##
    app.addLabelEntry("login_name")
    app.addSecretLabelEntry("login_password")
    app.addButton("submit", submit_login)
    app.addButton("cancel", cancel_button)
    app.stopTab()

    app.startTab("create_account_tab")  ## creates a create account tab##
    app.addLabelEntry("create_account_name")
    app.addSecretLabelEntry("create_account_password")
    app.addSecretLabelEntry("confirm_password")
    app.addLabelEntry("create_account_email")
    app.addButton("submit_", submit_create_account)
    app.addButton("cancel_", cancel_button)
    app.stopTab()
    app.stopTabbedFrame()
    #app.stopSubWindow()

    app.startSubWindow("menu_after_login")

    app.startTabbedFrame("bookings_and_review_tab")

    app.startTab("BOOKING")
    app.addLabel("check in: ")
    app.addDatePicker("check_in")##### adds a date picker for check in
    app.setDatePickerRange("check_in", now, now + 1)#### takes the current year using the date time
    app.setDatePicker("check_in")######################## library and uses that to show the years in
    app.addLabel("check out: ")
    app.addDatePicker("check_out")####################### date picker
    app.setDatePickerRange("check_out", now, now + 1)
    app.setDatePicker("check_out")
    app.addLabelSpinBoxRange("adults", 1, 12)######adds option box for number of
    app.addLabelSpinBoxRange("children", 1, 12)#####adults and children
    app.addLabel("extras")
    app.addCheckBox("breckfast")
    app.addCheckBox("lunch")
    app.addCheckBox("dinner")
    app.addCheckBox("wi-fi")
    app.addButton("CONFIRM", submit_bookings_system)
    app.stopTab()


    app.startTab("REVIEW")
    app.addLabel("REVIEWSECTION")
    app.stopTab()
    app.stopTabbedFrame()

    app.stopSubWindow()

    app.startSubWindow("payment_system")
    app.addLabelEntry("card_number")
    app.addLabelEntry("name_on_card")
    app.addLabelSpinBoxRange("expiration_month", 1, 12)
    app.addLabel("/")
    app.addSpinBoxRange("expiration_year", now, now+10)
    app.addLabelEntry("cvv")
    app.addButton("confirm",confirm_payment)
    app.addButton("cancel__",cancel_button)
    app.stopSubWindow()

def confirm_payment():
    card_number = app.getEntry("card_number")
    name_on_card =  app.getEntry("name_on_card")
    expiration_month = app.getSpinBox("expiration_month")
    expiration_year = app.getSpinBox("expiration_year")
    cvv = app.getEntry("cvv")
    expiration_date = str(expiration_month+"/"+expiration_year)
    if len(card_number) != 16:
        app.warningBox("ERROR", "NOT VALID CARD NUMBER")
    if len(cvv) != 3:
        app.warningBox("ERROR", "NOT VALID CVV")
    else:
        print("send to db")


def submit_bookings_system():
    check_in = app.getDatePicker("check_in")
    check_out = app.getDatePicker("check_out")
    number_adults =  app.getSpinBox("adults")
    number_children = app.getSpinBox("children")
    breckfast = app.getCheckBox("breckfast")
    lunch = app.getCheckBox("lunch")
    dinner = app.getCheckBox("dinner")
    wifi = app.getCheckBox("wi-fi")

    if check_in>check_out:
        app.warningBox("ERROR", "CHECK-IN DATE LESS THAN CHECK OUT DATE")
    else:
        app.showSubWindow("payment_system")



def submit_login():
    name = app.getEntry("login_name")  ## takes the name and password from create_interface() ##
    password = app.getEntry("login_password")
    cur.execute("SELECT d_name, d_password FROM user_table WHERE d_name= ?",(name, ))#
    user_db=cur.fetchone()
    if user_db == None:
        app.warningBox("LOGIN ERROR", "INCORRECT USERNAME OR PASSWORD")
    elif user_db[1] != password:
        app.warningBox("LOGIN ERROR", "INCORRECT USERNAME OR PASSWORD")
    else:
        app.infoBox("LOGIN", "LOGIN SUCCSEFUL", parent=None)
        app.showSubWindow("menu_after_login")


def submit_create_account():
    ######takes entries from create interface in create account tab#####
    name = app.getEntry("create_account_name")
    password = app.getEntry("create_account_password")
    confirm_password = app.getEntry("confirm_password")
    email = app.getEntry("create_account_email")
    #####validation#####
    if len(name)<3 or len(name)>10:####validatename#####
        app.warningBox("ERROR WITH NAME", "Length must be between 3 and 10 characters", parent=None)
    if  len(password)<5:####validate password length####
        app.warningBox("ERROR WITH PASSWORD", "Length of password too short, must be above 5 characters", parent =None)
    if password != confirm_password:####checks to see if passwords are equal####
        app.warningBox("ERROR WITH PASSWORD", "Passwords not equal", parent=None)
    if not (re.search(regex,email)): ####checks the format of email##### ###taken from _________________________________________ website
        app.warningBox("ERROR WITH EMAIL", "Not Valid Email",parent=None)
    else:
        sql = "INSERT INTO user_table (d_name,d_password,email) VALUES (?, ?, ?)"
        val = (name, password, email)#reference for lines 107,108,109 is w3schools
        cur.execute(sql, val)
        con.commit()#commits the user details to user_table
        app.infoBox("commited", "ACCOUNT HAS BEEN CREATED", parent=None)#popup showing user that their details are now in the database


def cancel_button():
    return

con = sqlite3.connect("nice_hotel_database.db", timeout=10)#connects to database needed
cur = con.cursor()
app=gui()
create_interface()
create_database()
app.go()
cur.close()