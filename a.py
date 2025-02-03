import mysql.connector
import datetime as d

mydb = mysql.connector.connect(
    host="127.0.0.1", 
    user="root",
    passwd="root",
    database="hotel",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

if mydb.is_connected():
    print("\nThe connection to server was successful.")
else:
    print("\nError! Server not connected.")

print("___________________________________________")
print("\n--------- Welcome To Hotel ---------")
print("___________________________________________")

current_user = None

# Function to log user activity with exact date and time
def log_activity(username, action, details):
    current_time = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format for exact date and time
    sql = "INSERT INTO user_activity_log (username, action, action_time, details) VALUES (%s, %s, %s, %s)"
    val = (username, action, current_time, details)
    mycursor.execute(sql, val)
    mydb.commit()

def find_customer():
    searchby = input("Search Customer By \n1. Name \n2. Phone_No. \n3. Check_IN_Date \nEnter Your Choice:  ")

    if searchby == "1":
        name = input("Enter Name: ")
        sql = "SELECT * FROM customers WHERE name = %s"
        val = (name,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()

        if result:
            print("Customer Data Found")
            for row in result:
                print("|| Customer ID : ", row[0], ",|| Customer Name :", row[1], "|| Phone No :", row[2], "|| ID PROOF :", row[3], "|| ID PROOF NO_ : ", row[4], "|| Room No. :", row[5], "|| Age :", row[6], "|| Check_IN_Date :", row[7], ",|| Check_OUT_Date :", row[8])
        else:
            print("No customer found with that name.")

    elif searchby == "2":
        phone_no = input("Enter Phone No.: ")
        sql = "SELECT * FROM customers WHERE phone_no = %s"
        val = (phone_no,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            for row in result:
                print(row)
        else:
            print("No customer found with that phone number.")

    elif searchby == "3":
        check_in_date = input("Enter Check In Date (YYYY-MM-DD) : ")
        sql = "SELECT * FROM customers WHERE check_in_date = %s"
        val = (check_in_date,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            for row in result:
                print(row)
        else:
            print("No customers found with that check-in date.")
    else:
        print("\nInvalid choice.")

# Function to login
def login():
    global current_user
    username = input("\nEnter username: ")
    password = input("\nEnter password: ")
    
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result:
        current_user = username
        print(f"\nWelcome, {current_user} !")
        log_activity(current_user, "Logged In", "User  logged in successfully.")
        return True
    else:
        print("\nInvalid username or password.")
        return False

# Function to register new users
def register():
    sql = "SELECT ROLE FROM users WHERE username = %s"
    val = (current_user,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result == 'admin':
        uid = input("\nEnter NEW ID: ")
        username = input("\nCreate new username : ")
        password = input("\nCreate new password : ")
        role = input("\nEnter role of the user : ")

        sql = "INSERT INTO users (id, username, password, role) VALUES (%s,%s,%s,%s)"
        val = (uid, username, password, role)
        mycursor.execute(sql, val)
        mydb.commit()
        print("\nRegistration successful!")
        
        # Log the registration action
        log_activity(current_user, "Registered a new user", f"New user created with username: {username}")
    else:
        print("\nYou are not authorized to register new users.")

# Function to view all users
def view_users():

    sql = "SELECT ROLE FROM users WHERE username = %s"
    val = (current_user,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result == 'admin':

        sql = "SELECT id, username, roll FROM users"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for row in result:
            print(row)
    
    else :
        print("\nYou are not authorized to view all users.")
    # Log the action
    log_activity(current_user, "Viewed all users", "User  viewed all registered users.")

# Function to delete a user
def delete_user():
    
    sql = "SELECT ROLE FROM users WHERE username = %s"
    val = (current_user,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    if result == 'admin':

        username = input("\nEnter username of user to delete: ")
        sql = "DELETE FROM users WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        mydb.commit()
        print("\nUser  deleted successfully.")

    else:
        print("\nYou are not authorized to delete users.")
    
    # Log the delete action
    log_activity(current_user, "Deleted a user", f"User  with username: {username} deleted.")

# Function to add a room
def add_room():
    room_no = int(input("Enter Room Number: "))
    room_type = input("Enter Room Type (Single, Deluxe, Suite, Luxury): ")
    room_price = float(input("Enter Room Price: "))
    room_status = input("Enter Room Status (Available/Occupied): ")

    sql = "INSERT INTO rooms (room_no, room_type, room_price, room_status) VALUES (%s, %s, %s, %s)"
    val = (room_no, room_type, room_price, room_status)
    mycursor.execute(sql, val)

    if current_user:
        sql = "UPDATE rooms SET modified_by = %s WHERE room_no = %s"
        mycursor.execute(sql, (current_user, room_no))
    
    mydb.commit()
    print("\n--------- Room added successfully ---------")

    # Log the room addition
    log_activity(current_user, "Added a room", f"Room No: {room_no}, Type: {room_type}")

# Function to check in a customer
def check_in():
    customer_name = input("Enter Customer's Name: ")
    customer_phone = input("Enter Customer's Phone Number: ")
    customer_id_proof = input("Enter Customer's ID Proof: ")
    customer_id_proof_no = int(input("Enter Customer's ID Proof Number: "))
    room_no = int(input("Enter Room Number: "))
    customer_age = int(input("Enter Customer's Age: "))
    check_in_date = d.datetime.now()

    # Check if the room is available
    sql = "SELECT room_status FROM rooms WHERE room_no = %s"
    mycursor.execute(sql, (room_no,))
    room_status = mycursor.fetchone()

    if room_status and room_status[0] == "Available":
        sql = "INSERT INTO customers (name, phone_no, id_proof, id_proof_no, room_no, age, check_in_date, modified_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (customer_name, customer_phone, customer_id_proof, customer_id_proof_no, room_no, customer_age, check_in_date, current_user)
        mycursor.execute(sql, val)

        sql = "UPDATE rooms SET room_status = %s WHERE room_no = %s"
        val = ("Occupied", room_no)
        mycursor.execute(sql, val)

        if current_user:
            sql = "UPDATE customers SET modified_by = %s WHERE room_no = %s"
            mycursor.execute(sql, (current_user, room_no))
        
        mydb.commit()
        print("\n--------- Customer checked in successfully ---------")

        # Log the check-in
        log_activity(current_user, "Checked in a customer", f"Customer: {customer_name}, Room No: {room_no}")
    else:
        print("Room is not available for check-in.")

# Function to check out a customer
def check_out():
    room_no = int(input("Enter Room Number: "))
    phone = input("Enter customer's Phone no : ")

    sql = "SELECT name, room_price, check_in_date FROM rooms INNER JOIN customers ON rooms.room_no = customers.room_no WHERE customers.room_no = %s AND phone_no = %s and check_out_date IS NULL "
    val = (room_no,phone,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        name, room_price, check_in_date = result
        
        check_out_date = d.datetime.now()
        
        in_date = d.datetime(check_in_date.year, check_in_date.month, check_in_date.day)
        out_date = d.datetime(check_out_date.year, check_out_date.month, check_out_date.day)

        days_stayed = (out_date - in_date).days
        
        total_bill = room_price * days_stayed
        
        sql = "UPDATE customers SET check_out_date = %s, total_bill = %s, modified_by = %s WHERE room_no = %s"
        val = (check_out_date, total_bill, current_user, room_no)
        mycursor.execute(sql, val)

        sql = "UPDATE rooms SET room_status = %s WHERE room_no = %s"
        val = ("Available", room_no)
        mycursor.execute(sql, val)
        
        mydb.commit()
        print(f"\n--------- Customer checked out successfully. Customer name : {name} || Check in date : {check_in_date} || Check_out_date : {check_out_date} || Days Stayed : {days_stayed} || Total bill: {total_bill} ---------")
        
        log_activity(current_user, "Checked out a customer", f"Customer: {name}, Room No: {room_no}")
        
    else:
        print("Room not found.")

def show_available_rooms():
    sql = "SELECT * FROM rooms WHERE room_status='Available'"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result:
        print("Room Details:")
        for row in result:
            room_no, room_type, room_price, room_status, modified_by = row
            print("Room No:", room_no, "|| Room Type:", room_type, "|| Room Price:", room_price, "|| Room Status:", room_status, "||")
    else:
        print("\n--------- No rooms available ---------")

    # Log the action
    log_activity(current_user, "Viewed available rooms", "User  viewed available rooms.")

# Function to show occupied rooms
def show_occupied_rooms():
    sql = "SELECT * FROM rooms WHERE room_status='Occupied'"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result:
        print("Room Details:")
        for row in result:
            room_no, room_type, room_price, room_status, modified_by = row
            print("Room No:", room_no, "|| Room Type:", room_type, "|| Room Price:", room_price, "|| Room Status:", room_status, "||")
    else:
        print("\n--------- No rooms found ---------")

    # Log the action
    log_activity(current_user, "Viewed occupied rooms", "User  viewed occupied rooms.")

def log():
    print("\n--------- Room Management System Log ---------")
    sql = "SELECT * FROM logs ORDER BY log_id DESC "
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for row in result:
        log_id, user_id, activity, description = row

        print(row)

# Main menu loop
while True:
    if login():
        while True: 
            choice = input("\nChoose an option:\n1. Register Staff \n2. Add Room\n3. Check In\n4. Check Out\n5. Show Available Rooms\n6. Show Occupied Rooms\n7. Find Customer \n8. View All Users\n9. Delete a user\n10. Vie Logs \n11. Logout\n12. Exit\n")

            if choice == "1":
                register()

            elif choice == '2':
                add_room()

            elif choice == '3':
                check_in()

            elif choice == '4':
                check_out()

            elif choice == '5':
                show_available_rooms()

            elif choice == '6':
                show_occupied_rooms()

            elif choice == '7':
                find_customer()

            elif choice == '8':
                view_users()

            elif choice == '9':
                delete_user()

            elif choice == '10':
                log()

            elif choice == '11':
                log_activity(current_user, "Logged Out", "User  logged out successfully.")
                break  # Exiting the loop

            elif choice == '12':
                log_activity(current_user, "closed program", "User  closed program successfully.")
                exit()

            else:
                print("--------- Invalid choice ---------")
