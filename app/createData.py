import sqlite3
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np


try:
    conn = sqlite3.connect('DB/bib.db')
    c = conn.cursor()
except Exception:
    print("Error when connecting to DB")

sns.set_style("whitegrid")
blue, = sns.color_palette("muted", 1)

svgStart = '<svg version="1.1" viewBox="0 0 792 360"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'


def fixSVG(string):
    svg = string.split('xmlns:xlink="http://www.w3.org/1999/xlink">', 1)[1]
    svg = svgStart + svg
    return svg



def getLastYear():

    c.execute('SELECT strftime("%Y-%m-%d",auslastung.Daytime) as day, avg(auslastung.Belegt) as belegt FROM auslastung where datetime(auslastung.Daytime) >=datetime("now", "-365 days")  group by day')

    alist = c.fetchall()
    df = pd.DataFrame(alist)


    df['datetime'] = pd.to_datetime(df[0])


    fig, ax = plt.subplots(figsize=(11, 5))
    date = df['datetime']
    belegt = df[1]
    plt.plot(date, belegt)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    formatter = mdates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    plt.fill_between(date, 0, belegt, alpha=.3)
    plt.legend(["Average occupancy in %"], loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())

def getLastYearBib(name):

    fields = [name]
    c.execute('SELECT strftime("%Y-%m-%d",auslastung.Daytime) as day,  avg(auslastung.Belegt) as belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? and datetime(auslastung.Daytime) >=datetime("now", "-365 days")  group by day ', fields)

    alist = c.fetchall()
    df = pd.DataFrame(alist)


    df['datetime'] = pd.to_datetime(df[0])


    fig, ax = plt.subplots(figsize=(11, 5))
    date = df['datetime']
    belegt = df[1]
    plt.plot(date, belegt)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    formatter = mdates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(formatter)
    plt.fill_between(date, 0, belegt, alpha=.3)
    plt.legend(["Average occupancy in %"], loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()

    plt.show()
    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())

getLastYearBib("FBHistoricum")


def getAllCurrent():
    c.execute(
        'SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort order by auslastung.Daytime desc limit 1000')
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
        c.execute(
            'SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? order by auslastung.Daytime desc limit ?',
            fields)
    else:
        c.execute(
            'SELECT auslastung.Daytime, bibs.RealName, auslastung.Belegt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? and (strftime("%M", auslastung.Daytime) == "00") order by auslastung.Daytime desc limit ?',
            fields)

    alist = c.fetchall()
    df = pd.DataFrame(alist)

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


def horBar():
    category_names = ['Not available', 'Available']

    c.execute(
        'SELECT auslastung.Daytime, bibs.RealName, bibs.CutName, auslastung.Belegt, auslastung.Frei, auslastung.Beschraenkt FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where auslastung.Daytime = (select Daytime from auslastung order by PK desc limit 1)')
    alist = c.fetchall()
    df = pd.DataFrame(alist)
    df.drop(columns=[0, 2, 5], inplace=True)
    results = df.set_index(1).T.to_dict('list')

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plt.tight_layout()
    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())

def getAverageHalfDay():
    c.execute(
        'SELECT avg(Belegt), Daytime FROM auslastung WHERE  datetime(Daytime) >=datetime("now", "-12 Hour") GROUP BY strftime ("%H:%M %d",Daytime) order by PK desc')
    alist = c.fetchall()
    df = pd.DataFrame(alist)

    df['datetime'] = pd.to_datetime(df[1])

    fig, ax = plt.subplots(figsize=(11, 5))
    date = df['datetime']
    belegt = df[0]

    # border = np.ma.masked_where(date.dt.hour < 8, belegt)

    plt.plot(date, belegt)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    formatter = mdates.DateFormatter('%d.%m. %H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.fill_between(date, 0, belegt, alpha=.3)
    plt.legend(["Average occupancy for all libraries in %"], loc='upper left')
    fig.autofmt_xdate()
    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    plt.close(fig)
    return fixSVG(f.getvalue())


def avergagebyWeekday():
    c.execute('select round(avg(belegt),2),  round(avg(beschraenkt),2), case cast (strftime("%w", Daytime) as integer) when 0 then "Sunday" when 1 then "Monday" when 2 then "Tuesday" when 3 then "Wednesday" when 4 then "Thursday" when 5 then "Friday" else "Saturday" end as servdayofweek from auslastung group by strftime("%w", Daytime) ')
    alist = c.fetchall()
    df = pd.DataFrame(alist)

    ind = df[2]  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.subplots(figsize=(11, 5))
    p1 = plt.bar(ind, df[0]*(1-df[1]), width)
    p2 = plt.bar(ind, df[0]*df[1], width,
                 bottom=df[0]*(1-df[1]))

    plt.ylabel('Occupancy in %')

    plt.legend((p1[0], p2[0]), ('Open to public', 'Faculty only'))

    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())


def avergagebyWeekdayLastTwoWeeks():
    c.execute('select round(avg(belegt),2),  round(avg(beschraenkt),2), case cast (strftime("%w", Daytime) as integer) when 0 then "Sunday" when 1 then "Monday" when 2 then "Tuesday" when 3 then "Wednesday" when 4 then "Thursday" when 5 then "Friday" else "Saturday" end as servdayofweek from auslastung where datetime(auslastung.Daytime) >=datetime("now", "-14 days")group by strftime("%w", Daytime) ')
    alist = c.fetchall()
    df = pd.DataFrame(alist)

    ind = df[2]  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.subplots(figsize=(11, 5))
    p1 = plt.bar(ind, df[0]*(1-df[1]), width)
    p2 = plt.bar(ind, df[0]*df[1], width,
                 bottom=df[0]*(1-df[1]))

    plt.ylabel('Occupancy in %')

    plt.legend((p1[0], p2[0]), ('Open to public', 'Faculty only'))

    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())


def avgbyWkdayByBib(name):
    fields = [name]
    c.execute('SELECT round(avg(auslastung.belegt),2), round(avg(auslastung.beschraenkt),2),  case cast (strftime("%w", auslastung.Daytime) as integer) when 0 then "Sunday" when 1 then "Monday" when 2 then "Tuesday" when 3 then "Wednesday" when 4 then "Thursday" when 5 then "Friday" else "Saturday" end as servdayofweek FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? group by strftime("%w", auslastung.Daytime)' , fields)
    alist = c.fetchall()
    df = pd.DataFrame(alist)


    ind = df[2]  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.subplots(figsize=(11, 5))
    p1 = plt.bar(ind, df[0]*(1-df[1]), width)
    p2 = plt.bar(ind, df[0]*df[1], width,
                 bottom=df[0]*(1-df[1]))

    plt.ylabel('Occupancy in %')

    plt.legend((p1[0], p2[0]), ('Open to public', 'Faculty only'))

    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())


def avgbyWkdayByBibLastTwoWeeks(name):
    fields = [name]
    c.execute('SELECT round(avg(auslastung.belegt),2), round(avg(auslastung.beschraenkt),2),  case cast (strftime("%w", auslastung.Daytime) as integer) when 0 then "Sunday" when 1 then "Monday" when 2 then "Tuesday" when 3 then "Wednesday" when 4 then "Thursday" when 5 then "Friday" else "Saturday" end as servdayofweek FROM auslastung INNER JOIN bibs ON bibs.PK = auslastung.Ort where bibs.CutName = ? and datetime(auslastung.Daytime) >=datetime("now", "-14 days") group by strftime("%w", auslastung.Daytime)' , fields)
    alist = c.fetchall()
    df = pd.DataFrame(alist)


    ind = df[2]  # the x locations for the groups
    width = 0.5  # the width of the bars: can also be len(x) sequence

    plt.subplots(figsize=(11, 5))
    p1 = plt.bar(ind, df[0]*(1-df[1]), width)
    p2 = plt.bar(ind, df[0]*df[1], width,
                 bottom=df[0]*(1-df[1]))

    plt.ylabel('Occupancy in %')

    plt.legend((p1[0], p2[0]), ('Open to public', 'Faculty only'))

    plt.tight_layout()

    f = io.StringIO()
    plt.savefig(f, format="svg")
    return fixSVG(f.getvalue())
