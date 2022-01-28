from datetime import date, timedelta
import mariadb
import random


def database_connect(name, count):
    # connects to db and return given connection object
    # count variable stands for how many tries should function procceed before turning of
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database=name
        )
    # if connection fails
    except mariadb.Error as e:
        print("dd", e)
        # dangerous!! can cycle forever if connection is not made exit program
    # return connection to given database
    return conn

def insert_data(data, conn):
    """
    Insert values from last day to sensors_history db
    """
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO sensors_history(water_height, soil_humidity, meas_date) VALUES (?, ?, ?)", 
                    (data[0], data[1], data[2]))
    except mariadb.Error as e:
        print("dd", e)
    conn.commit()


def main():
    conn = database_connect("watering", 0)
    data = [None] * 3
    for i in range(250):
        data[0] = random.randint(0, 100)
        data[1] = random.randint(0, 100)
        data[2] = date.today() - timedelta(days = i + 8)
        insert_data(data, conn)

main()