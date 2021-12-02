import socket
import sys
import mariadb

args = sys.argv[1:]

def read_database(limit):
    soil_list = []
    water_list = []
    # read values from given database by given limit
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
    try:
        curr.execute(f"SELECT id, soil_humidity, water_height FROM sensors ORDER BY id DESC LIMIT {limit}")
    except mariadb.Error as e:
        print(f"Could not get data from database: {e}")
    for soil_humidity, water_height in curr:
        soil_list.append(soil_humidity)
        water_list.append(water_height)
        
    return(soil_list, water_list)


def water():
    pass

def main():
    pass

print("lojza")