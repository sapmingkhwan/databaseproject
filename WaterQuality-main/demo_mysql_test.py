import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "testingdb"
)
mycursor = mydb.cursor()

#mycursor.execute('CREATE DATABASE testingdb')

#mycursor.execute("CREATE TABLE account (id INT AUTO_INCREMENT PRIMARY KEY, fullname VARCHAR(255), username VARCHAR(255), password VARCHAR(255), email VARCHAR(255))")
mycursor.execute("CREATE TABLE data (id INT AUTO_INCREMENT PRIMARY KEY, ph VARCHAR(200), dissolved_oxygen VARCHAR(200), turbidity VARCHAR(200), ec VARCHAR(200))")

sql = "INSERT INTO data (ph, dissolvd_oxygen, turbidty, ec) VALUES (%s, %s, %s, %s)"
val = []
mycursor.execute(sql, val)