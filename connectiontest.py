import mysql.connector

# db = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "",
#     #database = "testingxampp"
# )
# mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE testingxampp")
# mycursor.execute("CREATE TABLE sd (name VARCHAR(50), age int UNSIGNED, sdID int PRIMARY KEY)")
# mycursor.execute("DESCRIBE sd")
# for x in mycursor:
#     print(x)

def connection():
        conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "taxisystem"
        )

        mycursor = conn.cursor()

        

        insertquery= "insert into userinfo (name, email,phone_num,password) VALUES (%s,%s,%s,%s)"
        values = ("sdf","sdf","er","34545")

        mycursor.execute(insertquery,values)

        conn.commit()
connection()


