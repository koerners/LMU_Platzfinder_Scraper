import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback
import sqlite3
import pandas as pd
import requests

try:
    conn = sqlite3.connect('DB/bib.db')
    c = conn.cursor()
except Exception:
    print(traceback.print_exc())

page = requests.get("https://www.ub.uni-muenchen.de/arbeiten/platzfinder/index.html")
pattern = re.compile("(?<=google.visualization.arrayToDataTable\(\[)(.*)(?=\]\);)")


def scrape():
    now = datetime.now()  # current date and time
    daytime = now.strftime("%Y-%m-%d %H:%M:%S")

    c.execute('SELECT PK, CutName from `bibs`')
    alist = c.fetchall()
    df = pd.DataFrame(alist)

    soup = BeautifulSoup(page.content, 'html.parser')

    frames = soup.findAll('iframe')

    for frame in frames:

        page2 = requests.get(frame.attrs['src'])
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        string = pattern.findall(soup2.text)[0]
        wortListe = string.replace(']', '').replace('[', '').replace(' ', '').replace('\'', '').split(',')

        if wortListe[0] == "Lesesaal":

            lesesaal = wortListe[3]
            lesesaalNr = df.loc[df[1] == lesesaal, 0].iloc[0]
            belegt = wortListe[-2]
            frei = wortListe[-1]
            beschraenkt = False

            if wortListe[2] != "freiePlätze":
                beschraenkt = True

            fields = [daytime, int(lesesaalNr), belegt, frei, beschraenkt]

            c.execute(
                "INSERT INTO `auslastung`(`Daytime`,`Ort`,`Belegt`,`Frei`,`Beschraenkt`) VALUES (?, ?, ?, ?,?);",
                fields)

            conn.commit()

    conn.close()


try:
    scrape()
    r = requests.get('https://api2.platzfinder.com/reload')
    print("Finished")
except Exception:
    print(traceback.print_exc())
