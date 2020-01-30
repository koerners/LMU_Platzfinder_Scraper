import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import csv
from notify_run import Notify
import traceback

page = requests.get("https://www.ub.uni-muenchen.de/arbeiten/platzfinder/index.html")
pattern = re.compile("(?<=google.visualization.arrayToDataTable\(\[)(.*)(?=\]\);)")


def sendNotification(message):
    try:
        notify = Notify()
        notify.send(message)
    except Exception:
        print(traceback.print_exc())


def scrape():
    now = datetime.now()  # current date and time
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M:%S")
    hour = now.time().hour
    minute = now.time().minute


    if hour < 8:
        return


    soup = BeautifulSoup(page.content, 'html.parser')

    frames = soup.findAll('iframe')

    auslastung = 0

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
                beschraenkt = True;

            if int(belegt) > 5:
                auslastung += int(belegt)

            fields = [date, time, lesesaal, belegt, frei, beschraenkt]
            with open(r'log.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    avg_auslastung = str(round(auslastung / len(frames), 2))

    if hour == 11 & minute < 30:
        sendNotification("AVG Auslastung: " + avg_auslastung)


try:
    scrape()
except Exception:
    print(traceback.print_exc())
    sendNotification("Fehler bei Scraper aufgetreten")
