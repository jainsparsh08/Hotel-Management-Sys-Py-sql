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
    print("\nThe connection to server was successful. ")
else:
    print("\nError! Server not connected.")

print ("___________________________________________")


print ("\n--------- Welcome To Hotel ---------")

print ("___________________________________________")



current_user = None

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
        return True
    else:
        print("\nInvalid username or password.")
        return False

def add_room():
    room_no = int(input("Enter Room Number: "))
    room_type = input("Enter Room Type ( Single, Deluxe, Suite, Luxury ): ")
    room_price = float(input("Enter Room Price: "))
    room_status = input("Enter Room Status (Available/Occupied): ")

    sql = "INSERT INTO rooms (room_no, room_type, room_price, room_status) VALUES (%s, %s, %s, %s)"
    val = (room_no, room_type, room_price, room_status)
    mycursor.execute(sql, val)
    
    # Add username of the user who added the room
    if current_user:
        sql = "UPDATE rooms SET modified_by = %s WHERE room_no = %s"
        mycursor.execute(sql, (current_user, room_no))
    
    mydb.commit()
    print("\n--------- Room added successfully ---------")

def check_in():
    customer_name = input("Enter Customer's Name: ")
    customer_phone = (input("Enter Customer's Phone Number: "))
    customer_id_proof = input("Enter Customer's ID Proof: ")
    customer_id_proof_no = int(input("Enter Customer's ID Proof Number: "))
    room_no = int(input("Enter Room Number: "))
    customer_age = int(input("Enter Customer's Age: "))
    check_in_date = d.datetime.now()

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

def check_out():
    room_no = int(input("Enter Room Number: "))

    sql = "SELECT room_price, check_in_date FROM rooms INNER JOIN customers ON rooms.room_no = customers.room_no WHERE customers.room_no = %s"
    val = (room_no,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        room_price, check_in_date = result
        
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
        print(f"\n--------- Customer checked out successfully. Total bill: {total_bill} ---------")
    else:
        print("Room not found.")


def show_available_rooms():
    sql = "SELECT * FROM rooms WHERE room_status='Available'"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result:
        print("Room Details:")
        for row in result:
            room_no, room_type, room_price, room_status, modified_by= row
            print("Room No:", room_no, "|| Room Type:", room_type, "|| Room Price:", room_price, "|| Room Status:", room_status,"||")
    else:
        print("\n--------- No rooms available ---------")
        


def show_occupied_rooms():
    sql = "SELECT * FROM rooms WHERE room_status='Occupied'"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    if result:
        print("Room Details:")
        for row in result:
            room_no, room_type, room_price, room_status, modified_by = row
            print("Room No:", room_no, "|| Room Type:", room_type, "|| Room Price:", room_price, "|| Room Status:", room_status,"||")

    else:
        print("\n--------- No rooms found ---------")



while True:

    if login():
        while True: 

            choice = input("\nChoose an option:\n1. Add Room\n2. Check In\n3. Check Out\n4. Show Available Rooms\n5. Show Occupied Rooms\n6. Quit\n\n")

            if choice == '1':
                add_room()

            elif choice == '2':
                check_in()

            elif choice == '3':
                check_out()

            elif choice == '4':
                show_available_rooms()

            elif choice == '5':
                show_occupied_rooms()

            elif choice == '6':
                break

            else:
                 print("--------- Invalid choice ---------")


