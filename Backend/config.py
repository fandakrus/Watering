import mariadb
import logging
from time import sleep
import sys

logging.basicConfig(filename="/var/log/python-log/error-log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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
        logging.info(f"Successfully connected to database {name}")
    # if connection fails
    except mariadb.Error as e:
        if count <= 100:
            logging.critical("Could not connect to DB")
            sys.exit(1)
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        count += 1
        sleep(5)
        # dangerous!! can cycle forever if connection is not made exit program
        return database_connect(name, count)
    # return connection to given database
    return conn


# creates global instance cursor to be used in whole program
conn = database_connect("watering", 0)



