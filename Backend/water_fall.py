from optparse import Option
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
# import logging


# logging.basicConfig(filename="/var/log/python-log/rain-read-log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def extract_number(data):
    if data == "neměřitelné" or data == '':
        return 0
    try:
        return float(data.split()[0].replace(',', '.'))
    except ValueError as e:
        # logging.error(f"Data in record is not number or anyting expected and error is: {e}")
        raise OSError
    
    


class WaterFallData:
    def __init__(self) -> None:
        self.record = None

    def get_html(self):
        try:
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        except FileNotFoundError as e:
            # logging.error(f"Could not open new browser tab with error: {e}")
            raise OSError
        browser.get("https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/srazky")
        self.html = browser.page_source
        time.sleep(2)
        browser.close()
        

    def get_record(self):
        soup = BeautifulSoup(self.html, features="html.parser")
        table = soup.findAll("table", attrs={"style": "border-top: solid #14387f 1pt; border-bottom: solid #14387f 1pt"})[1]
        if table == []:
            # logging.info("No table found in recieved html code")
            raise OSError
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = [td.get_text() for td in row.find_all("td")]
            datasets.append(dataset)
        try:
            self.record = datasets[5]
        except IndexError as e:
            # logging.info("Dataset from table is find properly with error: {e}")
            raise OSError

    def get_rain_value(self):
        if self.record[0] != "Plzeň-Mikulka":
            # logging.error("Wrong dataset read from webpage")
            raise OSError
        self.rain = 0
        for i in range(2, 5):
            self.rain += extract_number(self.record[i])
        return self.rain
        
    def display_html(self):
        print(self.html)

    def display_record(self):
        print(self.record)



if __name__ == '__main__':
    klassa = WaterFallData()
    klassa.get_html()
    klassa.get_record()
    klassa.display_record()
    print(klassa.get_rain_value())