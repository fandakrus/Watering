from email.errors import MultipartInvariantViolationDefect
import mariadb
import logging
from time import sleep
import sys

logging.basicConfig(filename="/var/log/python-log/error-log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ConnClass:
    def __init__(self) -> None:
        self._connection = database_connect("watering", 0)

    def redo_connection(self):
        try:
            self._connection.reconnect()
            return
        except mariadb.Error as e:
            logging.error(f"config.py --- Could not reconnect to dabase because of error: {e}")
        try:
            self._connection.close()
            self._connection = database_connect("watering", 0)
            return
        except mariadb.Error as e:
            logging.critical(f"config.py --- Did not reach database with hard reconnection and error is: {e}")

    def get_connecion(self):
        try:
            self._connection.ping()
        except mariadb.Error:
            self.redo_connection()
        return self._connection


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
            logging.critical("config.py --- Could not connect to DB")
            sys.exit(1)
        logging.error(f"config.py --- Error connecting to MariaDB Platform: {e}")
        count += 1
        sleep(5)
        # dangerous!! can cycle forever if connection is not made exit program
        return database_connect(name, count)
    # return connection to given database
    return conn


connc = ConnClass()


