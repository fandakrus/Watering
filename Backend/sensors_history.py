import mariadb
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import date, timedelta
import os.path


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


def select_graph_data(conn):
    """
    Gets dates and water_height values from last year
    """
    curr = conn.cursor()
    try:
        curr.execute("SELECT water_height, meas_date FROM sensors_history ORDER BY meas_date DESC LIMIT 365")
    except mariadb.Error as e:
        logging.error(f"Could not read from sensor_history database because of error: {e}")
    data = list(map(list, zip(*curr.fetchall())))
    return data

def count_diff(length):
    # finds out how big spaces should be on x axe
    if length < 8:
        return 1
    return int(length/8)


def prepare_graph(data):
    """
    Gets two list of data and makes graph based on it
    """
    oldest = date.fromisoformat(str(min(data[1])))     # TODO repair this 
    newest = date.today()
    diff = count_diff(len(data[0]))
    fig, ax = plt.subplots(1, 1)
    ax.plot(data[1], data[0])
    ax.set_xticks(np.arange(oldest, newest, timedelta(days=diff)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d. %b"))
    fig.autofmt_xdate(rotation=90)
    fig.set_size_inches(20, 5)
    plt.savefig('/var/www/html/static/foo.png', dpi=150)



def main():
    connh = database_connect("watering", 0)
    logging.info("Sensors history script started trying to make new record")
    data = select_data(connh)
    if data is not None:
        insert_data(data, connh)
    else:
        logging.error("No data from sensor database recieved.")
    data = select_graph_data(connh)
    prepare_graph(data)
    connh.close()


if __name__ == "__main__":
    main()
