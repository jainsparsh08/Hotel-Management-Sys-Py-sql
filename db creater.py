import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="root",
    auth_plugin='mysql_native_password'

)

mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS hotel")
mydb.commit()

mycursor.execute("USE hotel")

mycursor.execute("CREATE TABLE IF NOT EXISTS rooms (room_no INT PRIMARY KEY, room_type VARCHAR(255), room_price DECIMAL(10, 2), room_status VARCHAR(255),modified_by varchar(50))")

mycursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), phone_no VARCHAR(20), id_proof VARCHAR(255), id_proof_no VARCHAR(20), room_no INT, age INT, check_in_date DATE, check_out_date DATE, bill_amount DECIMAL(10, 2), FOREIGN KEY (room_no) REFERENCES rooms(room_no),modified_by varchar(50))")

mycursor.execute("""CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    role VARCHAR(255) NOT NULL
);""")