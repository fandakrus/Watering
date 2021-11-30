import mariadb

try:
    conn = mariadb.connect(
            user="root",
            password="",
            host="192.168.0.193",
            port=3306,
            database="watering"
    )
    print("Connected to database")
# if connection fails
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
# create cursor object on given connection
curr = conn.cursor()
# insert values to database
curr.execute("INSERT INTO sensors(soil_humidity, water_height) VALUES (?, ?)", (2, 1))
# end the connection to database
conn.close()