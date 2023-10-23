import mysql.connector
from mysql.connector import Error
import pandas as pd4
import getEvent from extractPalminfo

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

event_info = """* **WashU Activities Fair**
    * Date: September 1, 2023
    * Time: 3:00 PM to 5:00 PM
    * Location: Mudd Field"""
sql = "INSERT INTO events (event_name, event_date, event_time, event_location) VALUES (%s, %s, %s, %s)"
event_data = (getEvent(event_info))
cursor.execute(sql, event_data)
create_teacher_table = """
CREATE TABLE teacher (
  teacher_id INT PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  language_1 VARCHAR(3) NOT NULL,
  language_2 VARCHAR(3),
  dob DATE,
  tax_id INT UNIQUE,
  phone_no VARCHAR(20)
  );
 """

pw='20031023'
db='module5Database'
connection = create_db_connection("localhost", "Dijkstra", pw, db) # Connect to the Database
execute_query(connection, create_teacher_table) # Execute our defined query