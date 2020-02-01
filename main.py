import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback
import sqlite3

conn = sqlite3.connect('bib.db')
c = conn.cursor()

page = requests.get("https://www.ub.uni-muenchen.de/arbeiten/platzfinder/index.html")
pattern = re.compile("(?<=google.visualization.arrayToDataTable\(\[)(.*)(?=\]\);)")


def scrape():
    now = datetime.now()  # current date and time
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M:%S")

    if now.time().hour < 8:
        return

    soup = BeautifulSoup(page.content, 'html.parser')

    frames = soup.findAll('iframe')

    for frame in frames:

        page2 = requests.get(frame.attrs['src'])
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        string = pattern.findall(soup2.text)[0]
        wortListe = string.replace(']', '').replace('[', '').replace(' ', '').replace('\'', '').split(',')

        if wortListe[0] == "Lesesaal":

            lesesaal = wortListe[3]
            belegt = wortListe[-2]
            frei = wortListe[-1]
            beschraenkt = False

            if wortListe[2] != "freiePlätze":
                beschraenkt = True

            fields = [date, time, lesesaal, belegt, frei, beschraenkt]

            c.execute(
                "INSERT INTO `auslastung`(`Day`,`Time`,`Ort`,`Belegt`,`Frei`,`Beschraenkt`) VALUES (?, ?, ?, ?, ?,?);",
                fields)

            conn.commit()

    conn.close()


try:
    scrape()
except Exception:
    print(traceback.print_exc())
