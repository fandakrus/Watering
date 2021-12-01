import mariadb

try:
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
# insert values to database
try:
    curr.execute("INSERT INTO sensors(soil_humidity, water_height) VALUES (?, ?)", (2, 1))
except mariadb.Error as e:
    print(f"Could not write in data because of error: {e}")


# curr.execute("SELECT soil_humidity, water_height FROM sensors")

conn.commit()

# end the connection to database
conn.close()