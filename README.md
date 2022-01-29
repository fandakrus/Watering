# Watering
Easy system using mainly python to control valves and water garden. 

# Functionality
The Backend/listener.py module is running on linux server and listening on desired port. Rest python files are just libraries. 
Php is used for simple control and data display using web application.
The sensors and relay are controled by esp32 running micorpython. The Micropython/Workspace/main.py is used on board.

# Hardware
Server is running on RPI3 with raspian. MariaDB is used. As microchip is used ESP32 and the lenght measurment sensor is HC-SR01 and for soil moisture is used analog capacitative sensor.

# Upgradabilty
Program is written for four valves control and one main valve. Amount of valves can be chaneg directly in code in watering.py. 