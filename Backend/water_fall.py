import requests
from bs4 import BeautifulSoup

class WaterFallData:
    def __init__(self) -> None:
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
        self.url = "https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/srazky"
        self.page_data = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.page_data.text, features="html.parser")
        with open('index.html', 'wb') as f:
            f.write(self.page_data.content)
        self.table = self.soup.findAll("li") # , attrs={"style": "border-top: solid #14387f 1pt; border-bottom: solid #14387f 1pt"}

    
    def display_html(self):
        print(self.page_data.text)

    
    def display_table(self):
        print(self.table)



if __name__ == '__main__':
    klassa = WaterFallData()
    klassa.display_table()