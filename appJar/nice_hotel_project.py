import sqlite3  # imports sql into python
import re
from PIL import Image, ImageTk

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
import datetime

now = datetime.datetime.now().year

from appjar import gui


def create_database():  # function that creates an empty database

    # creates the user table

    cur.execute("""CREATE TABLE IF NOT EXISTS user_table (
                user_id INTEGER PRIMARY KEY,
                d_name TEXT NOT NULL UNIQUE,
                d_password TEXT NOT NULL,
                email	TEXT NOT NULL UNIQUE
        );
    """)
    # creates the payment table
    cur.execute("""CREATE TABLE IF NOT EXISTS "payment_table" (
                "payment_id" INTEGER PRIMARY KEY,
                "user_id" INTEGER NOT NULL UNIQUE,
                "card_number" INTEGER NOT NULL UNIQUE,
                "name_on_card" TEXT NOT NULL ,
                "expiration_date" INTEGER NOT NULL,
                "cvv" INTEGER NOT NULL UNIQUE,
                FOREIGN KEY("user_id") REFERENCES "user_table"
                );
    """)
    # creates the bookings table
    cur.execute("""CREATE TABLE IF NOT EXISTS "booking_table" (
                    "booking_id" INTEGER PRIMARY KEY ,
                    "user_id" INTEGER NOT NULL,
                    "check_in" INTEGER NOT NULL,
                    "check_out"	INTEGER NOT NULL,
                    "number_of_adults"	INTEGER NOT NULL,
                    "number_of_children" INTEGER NOT NULL,
                    "breckfast"	INTEGER,
                    "lunch" INTEGER,
                    "dinner" INTEGER,
                    "wifi" INTEGER,
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
                    "review_id" INTEGER PRIMARY KEY,
                    "user_id" INTEGER NOT NULL UNIQUE,
                    "rating" INTEGER NOT NULL UNIQUE,
                    "user_review" TEXT NOT NULL UNIQUE
                    
                    
);
    """)


def create_interface():
    """
    app.startSubWindow("menu")
    app.showSubWindow("menu")
    app.setSize(700, 400)
    app.setResizable(canResize=False)
    app.addLabel("NICEHOTEL")
    app.startTabbedFrame("main_menu")  ## CREATES A TABBED FRAME##
    app.setTabbedFrameTabExpand("main_menu", expand=False)
    app.setSticky("main_menu")
    app.startTab("main_menu_tab")  ## creates a main menu tab ##
    app.addLabel("l1", "MAIN MENU")
    app.stopTab()

    app.startTab("login_tab")  ## creates a login tab##
    app.addLabelEntry("login_name")
    app.addSecretLabelEntry("login_password")
    app.addButton("submit", submit_login)
    app.addButton("cancel", cancel_button_login)
    app.stopTab()

    app.startTab("create_account_tab")  ## creates a create account tab##
    app.addLabelEntry("create_account_name")
    app.addSecretLabelEntry("create_account_password")
    app.addSecretLabelEntry("confirm_password")
    app.addLabelEntry("create_account_email")
    app.addButton("CREATE ACCOUNT", submit_create_account)
    app.addButton("CANCEL", cancel_button_create_account)
    app.stopTab()

    app.stopTabbedFrame()

    app.stopSubWindow()

    app.startSubWindow("menu_after_login")

    app.startTabbedFrame("bookings_menu")

    app.startTab("BOOKING")
    app.addLabel("check in: ")
    app.addDatePicker("check_in")  ##### adds a date picker for check in
    app.setDatePickerRange("check_in", now, now + 1)  #### takes the current year using the date time
    app.setDatePicker("check_in")  ######################## library and uses that to show the years in
    app.addLabel("check out: ")
    app.addDatePicker("check_out")  ####################### date picker
    app.setDatePickerRange("check_out", now, now + 1)
    app.setDatePicker("check_out")
    app.addLabelSpinBoxRange("adults", 1, 12)  ######adds option box for number of
    app.addLabelSpinBoxRange("children", 1, 12)  #####adults and children
    app.addLabel("extras")
    app.addCheckBox("breckfast")
    app.addCheckBox("lunch")
    app.addCheckBox("dinner")
    app.addCheckBox("wi-fi")
    app.addButton("CONFIRM", submit_bookings_system)
    app.stopTab()

    app.startTab("REVIEW")
    app.addLabelOptionBox("RATING", ["1","2","3","4","5"])
    app.addLabel("please leave a review:")
    app.addTextArea("review")
    app.addButton("WRITE REVIEW",write_review)
    app.addButton("CANCEL REVIEW",cancel_review)
    app.stopTab()

    app.stopTabbedFrame()

    app.stopSubWindow()

    app.startSubWindow("payment_system")

    app.addLabelEntry("card_number")
    app.addLabelEntry("name_on_card")
    app.addLabelSpinBoxRange("expiration_month", 1, 12)
    app.addLabel("/")
    app.addSpinBoxRange("expiration_year", now, now + 10)
    app.addLabelEntry("cvv")
    app.addButton("MAKE PAYMENT", confirm_payment)
    app.addButton("CANCEL PAYMENT", cancel_button_payment)

    app.stopSubWindow()
    """
    app.startSubWindow("menu")
    app.showSubWindow("menu")

    app.setSize("fullscreen")##########gui configuration of the programm
    app.setResizable(canResize=True)
    app.setPadding([20, 20])
    app.setSticky("nw")
    app.showTitleBar()

    app.setBg("white", override=False, tint=False)
    app.setFg("blue", override=False)

    photo = ImageTk.PhotoImage(Image.open("nicehotel_logo.jpg"))#####adds the image nice hotel image to it
    app.addImageData("pic", photo, fmt="PhotoImage")########code taken from appjar website

    app.addButton("LOGIN", load_login, 0, 1)
    app.addButton("exit", exit_program,0, 2)
    app.addLabel("review one","placeholder1",1,0)
    app.addLabel("review two ","placeholder2",2,0)
    app.addLabel("l5", "row=1\ncolumn=1", 1, 1)
    app.addLabel("l6", "row=1\ncolumn=2", 1, 2)
    app.addLabel("l8", "row=2\ncolumn=1", 2, 1)
    app.addLabel("l9", "row=2\ncolumn=2", 2, 2)
    app.button("leave a review", load_review,3,0)
    app.stopSubWindow()

    app.startSubWindow("login")
    app.setBg("white", override=False, tint=False)
    app.setLocation(1170,50)
    app.hideTitleBar()
    app.setSticky("ew")
    app.addLabel("name_label", "Name", 0, 0)
    app.addEntry("login_name", 0, 1)
    app.addLabel("password_label", "Password", 1, 0)
    app.addSecretEntry("login_password", 1, 1)
    app.addButtons(["Submit", "Cancel"], [submit_login, cancel_button_login], 2, 0, 2)
    app.addLink("create account here!", load_create_account)
    app.stopSubWindow()

    app.startSubWindow("create account")
    app.addLabelEntry("create_account_name")
    app.addSecretLabelEntry("create_account_password")
    app.addSecretLabelEntry("confirm_password")
    app.addLabelEntry("create_account_email")
    app.addButton("CREATE ACCOUNT", submit_create_account)
    app.addButton("CANCEL", cancel_button_create_account)
    app.stopSubWindow()

    app.startSubWindow("review")
    app.addLabelOptionBox("RATING", ["1", "2", "3", "4", "5"])
    app.addLabel("please leave a review:")
    app.addTextArea("review")
    app.addButton("WRITE REVIEW", write_review)
    app.addButton("CANCEL REVIEW", cancel_review)
    app.stopSubWindow()

    app.startSubWindow("booking")
    app.addLabel("check in: ")
    app.addDatePicker("check_in")  ##### adds a date picker for check in
    app.setDatePickerRange("check_in", now, now + 1)  #### takes the current year using the date time
    app.setDatePicker("check_in")  ######################## library and uses that to show the years in
    app.addLabel("check out: ")
    app.addDatePicker("check_out")  ####################### date picker
    app.setDatePickerRange("check_out", now, now + 1)
    app.setDatePicker("check_out")
    app.addLabelSpinBoxRange("adults", 1, 12)  ######adds option box for number of
    app.addLabelSpinBoxRange("children", 1, 12)  #####adults and children
    app.addLabel("extras")
    app.addCheckBox("breckfast")
    app.addCheckBox("lunch")
    app.addCheckBox("dinner")
    app.addCheckBox("wi-fi")
    app.addButton("CONFIRM", submit_bookings_system)
    app.addButton("CANCEL BOOKING", cancel_booking)
    app.stopSubWindow()

    app.startSubWindow("payment")
    app.addLabelEntry("card_number")
    app.addLabelEntry("name_on_card")
    app.addLabelSpinBoxRange("expiration_month", 1, 12)
    app.addLabel("/")
    app.addSpinBoxRange("expiration_year", now, now + 10)
    app.addLabelEntry("cvv")
    app.addButton("MAKE PAYMENT", confirm_payment)
    app.addButton("CANCEL PAYMENT", cancel_button_payment)
    app.stopSubWindow()


def write_review():
    rating = app.getOptionBox("RATING")
    review= app.getTextArea("review")
    if len(review)>250:
        app.warningBox("review","more than 250 characters")
    else:
        sql = "INSERT INTO review_table (user_id,rating,user_review) VALUES (?,?,?)"
        val = (user_id, rating, review)
        cur.execute(sql,val)
        con.commit()
        app.infoBox("review","added to databse")

def submit_login():
    global user_id
    name = app.getEntry("login_name")  ## takes the name and password from create_interface() ##
    password = app.getEntry("login_password")
    cur.execute("SELECT user_id, d_name, d_password FROM user_table WHERE d_name= ?", (name,))  #
    user_db = cur.fetchone()
    if user_db == None:
        app.warningBox("LOGIN ERROR", "INCORRECT USERNAME OR PASSWORD")
    elif user_db[2] != password:
        app.warningBox("LOGIN ERROR", "INCORRECT USERNAME OR PASSWORD")
    else:
        user_id = user_db[0]
        app.infoBox("LOGIN", "LOGIN SUCCSEFUL", parent=None)
        app.hideSubWindow("menu")
        app.hideSubWindow("login")
        app.showSubWindow("booking")

def submit_create_account():
    ######takes entries from create interface in create account tab#####
    name = app.getEntry("create_account_name")
    password = app.getEntry("create_account_password")
    confirm_password = app.getEntry("confirm_password")
    email = app.getEntry("create_account_email")
    #####validation#####
    if len(name) < 3 or len(name) > 10:  ####validatename#####
        app.warningBox("ERROR WITH NAME", "Length must be between 3 and 10 characters", parent=None)
    if len(password) < 5:  ####validate password length####
        app.warningBox("ERROR WITH PASSWORD", "Length of password too short, must be above 5 characters", parent=None)
    if password != confirm_password:  ####checks to see if passwords are equal####
        app.warningBox("ERROR WITH PASSWORD", "Passwords not equal", parent=None)
    if not (re.search(regex,email)):  ####checks the format of email##### ###taken from _________________________________________ website
        app.warningBox("ERROR WITH EMAIL", "Not Valid Email", parent=None)
    else:
        sql = "INSERT INTO user_table (d_name,d_password,email) VALUES (?, ?, ?)"
        val = (name, password, email)  # reference for lines 107,108,109 is w3schools
        cur.execute(sql, val)
        con.commit()  # commits the user details to user_table
        app.infoBox("commited", "ACCOUNT HAS BEEN CREATED",parent=None)  # popup showing user that their details are now in the database

def submit_bookings_system():
    check_in = app.getDatePicker("check_in")
    check_out = app.getDatePicker("check_out")
    number_adults = app.getSpinBox("adults")
    number_children = app.getSpinBox("children")
    breckfast = app.getCheckBox("breckfast")
    lunch = app.getCheckBox("lunch")
    dinner = app.getCheckBox("dinner")
    wifi = app.getCheckBox("wi-fi")

    if check_in > check_out:
        app.warningBox("ERROR", "CHECK-IN DATE LESS THAN CHECK OUT DATE")
    else:
        app.showSubWindow("payment")
        booking_details = (check_in, check_out, number_adults, number_children, breckfast, lunch, dinner,wifi)  ##creates a tuple with the booking details in it
        return booking_details  ####returns booking details to the function submit booking systems

def confirm_payment():
    card_number = app.getEntry("card_number")########takes card number
    name_on_card = app.getEntry("name_on_card")###takes the name on card
    expiration_month = app.getSpinBox("expiration_month")#takes the espiration month
    expiration_year = app.getSpinBox("expiration_year")#takes the expiration year
    cvv = app.getEntry("cvv")##takes the cvv number
    expiration_date = str(expiration_month + "/" + expiration_year)##puts expiration month and year
    if len(card_number) != 16:######################################together to make a date
        app.warningBox("ERROR", "NOT VALID CARD NUMBER")
    if len(cvv) != 3:
        app.warningBox("ERROR", "NOT VALID CVV")
    else:
        booking_details = submit_bookings_system()####takes the booking details from the function
        check_in = booking_details[0]#######splits the fucntion back into each variable
        check_out = booking_details[1]
        number_adults = booking_details[2]
        number_children = booking_details[3]
        breckfast = booking_details[4]
        lunch = booking_details[5]
        dinner = booking_details[6]
        wifi = booking_details[7]

        sqlbooking = "INSERT INTO booking_table (user_id,check_in,check_out,number_of_adults,number_of_children,breckfast,lunch,dinner,wifi) VALUES (?,?,?,?,?,?,?,?,?)"
        valbooking = (user_id,check_in, check_out, number_adults,number_children,breckfast,lunch,dinner,wifi)
        con.execute(sqlbooking, valbooking)
        sqlpayment ="INSERT INTO payment_table (user_id,card_number,name_on_card,expiration_date,cvv) VALUES (?,?,?,?,?)"################################
        valpayment =(user_id, card_number,name_on_card,expiration_date,cvv)
        con.execute(sqlpayment,valpayment)  # commits the user details to user_table
        con.commit()
        app.infoBox("COMMITED","added to database")
        app.hideSubWindow("payment")


def load_review():
    app.showSubWindow("review")

def load_login():
    app.showSubWindow("login")

def load_create_account():
    app.showSubWindow("create account")

def cancel_booking():
    app.showSubWindow("menu")
    app.hideSubWindow("booking")

def cancel_button_login():
    app.clearEntry("login_name", callFunction=False)
    app.clearEntry("login_password", callFunction=False)
    app.hideSubWindow("login")
    app.showSubWindow("menu")

def cancel_button_create_account():
    app.clearEntry("create_account_name", callFunction=False)
    app.clearEntry("create_account_password", callFunction=False)
    app.clearEntry("confirm_password", callFunction=False)
    app.clearEntry("create_account_email", callFunction=False)
    app.hideSubWindow("create account")
    app.showSubWindow("login")

def cancel_button_payment():
    app.clearEntry("card_number", callFunction=False)
    app.clearEntry("name_on_card", callFunction=False)
    app.clearSpinBox("expiration_month", callFunction=False)
    app.clearSpinBox("expiration_year", callFunction=False)
    app.clearEntry("create_account_name", callFunction=False)
    app.clearEntry("cvv", callFunction=False)
    app.hideSubWindow("payment")
    app.showSubWindow("booking")

def cancel_review():
    app.clearTextArea("review")##clears text area
    app.clearOptionBox("RATING")#sets the option box back to original value
    app.hideSubWindow("review")
    app.showSubWindow("menu")

def exit_program():
    exit()


con = sqlite3.connect("nice_hotel_database.db", timeout=10)  # connects to database needed
cur = con.cursor()
app = gui()

create_interface()
create_database()

app.go(startWindow="menu")

cur.close()
