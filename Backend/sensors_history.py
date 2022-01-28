import mariadb
import logging
from config import database_connect


logging.basicConfig(filename="/var/log/python-log/sensor-history-log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def select_data(conn):
    """
    Gets all records from sensor db that was made that day before
    """
    curr = conn.cursor()
    try:
        curr.execute("SELECT AVG(water_height), AVG(soil_humidity) FROM sensors WHERE DATE(meas_date) = SUBDATE(CURDATE(), 1)")
    except mariadb.Error as e:
        logging.error(f"Could not read from sensor_history database because of error: {e}") 
    data = curr.fetchone()
    curr.fetchall()
    conn.commit()
    return data

def insert_data(data, conn):
    """
    Insert values from last day to sensors_history db
    """
    water_height, soil_humidity = data
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO sensors_history(water_height, soil_humidity, meas_date) VALUES (?, ?, SUBDATE(CURDATE(), 1))", 
                    (water_height, soil_humidity))
    except mariadb.Error as e:
        logging.error(f"Could not write into sensor_history database because of error: {e}")
    conn.commit()


def main():
    connh = database_connect("watering", 0)
    logging.info("Sensors history script started trying to make new record")
    data = select_data(connh)
    if data is not None:
        insert_data(data, connh)
    else:
        logging.error("No data from sensor database recieved.")
    connh.close()


if __name__ == "__main__":
    main()
