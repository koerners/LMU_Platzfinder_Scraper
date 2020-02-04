import json
from klein import Klein
import sqlite3
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Klein()
resource = app.resource


conn = sqlite3.connect('bib.db')
c = conn.cursor()


sns.set_style("whitegrid")
blue, = sns.color_palette("muted", 1)

svgStart = '<svg version="1.1" viewBox="0 0 792 360"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'


def fixSVG(string):
    svg = string.split('xmlns:xlink="http://www.w3.org/1999/xlink">', 1)[1]
    svg = svgStart + svg
    return svg


def getAllCurrent():
    c.execute('SELECT * FROM `auslastung` order by PK desc limit 300')
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df['datetime'] = df[1].astype(str) + ' ' + df[2]
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.drop([0, 1, 2], axis=1, inplace=True)
    availableBibs = df[3].unique()

    fig = plt.figure(figsize=(11, 5))
    for bib in availableBibs:
        val = df.loc[df[3] == bib]
        date = val['datetime']
        belegt = val[4]
        plt.plot(date, belegt)
    plt.legend(availableBibs, loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()
    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())


def getSingleBib(name, limit):
    fields = [name, limit]
    c.execute('SELECT * FROM `auslastung` where Ort = ? order by PK desc limit ?', fields)
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df['datetime'] = df[1].astype(str) + ' ' + df[2]
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.drop([0, 1, 2], axis=1, inplace=True)

    fig = plt.figure()
    val = df
    date = val['datetime']
    belegt = val[4]
    plt.plot(date, belegt)
    plt.fill_between(date, 0, belegt, alpha=.3)
    plt.legend(["Occupancy in %"], loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()
    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())


def getCurrentStatus():
    c.execute(
        'select * from auslastung where Day = (select Day from auslastung order by PK desc limit 1) and Time = (select Time from auslastung order by PK desc limit 1)')
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df['datetime'] = df[1].astype(str) + ' ' + df[2]
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.drop([0, 1, 2], axis=1, inplace=True)
    return df.values.tolist()




@app.route('/')
def items(self):
    return ("Connected")


@app.route('/allGraph')
def itemsGraph(self):
    return getAllCurrent()


@app.route('/status')
def itemsStatus(self):
    return json.dumps(getCurrentStatus(), default=str)


@app.route('/bib/<string:name>/<string:limit>', methods=['GET'])
def get_item(self, name, limit):

    return getSingleBib(name, limit)

