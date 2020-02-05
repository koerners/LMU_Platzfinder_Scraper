import json
from klein import Klein
import sqlite3
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mtick


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
    c.execute('SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort order by auslastung.Daytime desc limit 1000')
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df['datetime'] = pd.to_datetime(df[0])

    availableBibs = df[1].unique()
    fig, ax = plt.subplots(figsize=(11, 5))

    for bib in availableBibs:
        val = df.loc[df[1] == bib]
        date = val['datetime']
        belegt = val[2]
        ax.plot(date, belegt)

    plt.legend(availableBibs, loc='upper left')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    formatter = mdates.DateFormatter('%d.%m. %H:%M')
    ax.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate()
    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())


def getSingleBib(name, limit):
    fields = [name, limit]

    if (int(limit) < 70):
        c.execute('SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? order by auslastung.Daytime desc limit ?', fields)
    else:
        c.execute('SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? and (strftime("%M", auslastung.Daytime) == "00") order by auslastung.Daytime desc limit ?',fields)

    alist = c.fetchall()
    df = pd.DataFrame(alist)

    print(df)

    df['datetime'] = pd.to_datetime(df[0])

    fig, ax = plt.subplots(figsize=(11, 5))
    date = df['datetime']
    belegt = df[2]
    plt.plot(date, belegt)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    formatter = mdates.DateFormatter('%d.%m. %H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.fill_between(date, 0, belegt, alpha=.3)
    plt.legend(["Occupancy in %"], loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()


    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())


def getCurrentStatus():
    c.execute(
        'SELECT auslastung.Daytime, bibs.RealName, bibs.CutName, auslastung.Belegt, auslastung.Frei, auslastung.Beschraenkt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where auslastung.Daytime = (select Daytime from auslastung order by PK desc limit 1)')
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df[0] = pd.to_datetime(df[0])
    return df.values.tolist()


@app.route('/')
def items(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return ("Connected")


@app.route('/allGraph')
def itemsGraph(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getAllCurrent()


@app.route('/status')
def itemsStatus(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    self.setHeader('Content-Type', 'application/json')
    return json.dumps(getCurrentStatus(), default=str)


@app.route('/bib/<string:name>/<string:limit>', methods=['GET'])
def get_item(self, name, limit):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getSingleBib(name, limit)

