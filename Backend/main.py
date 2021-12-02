import socket
import sys
import mariadb

args = sys.argv[1:]

def read_database():
    # read values from given database
    try:                         #connect to database -  password needs to be inserted
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="watering"
    )
        print("Connected to database")
    # if connection fails
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    # create cursor object on given connection
    curr = conn.cursor()
    
    pass

def water():
    pass

def main():
    pass

print("lojza")