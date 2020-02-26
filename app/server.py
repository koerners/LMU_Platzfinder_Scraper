import json
from klein import Klein
from createData import *

app = Klein()
resource = app.resource

@app.route('/')
def items(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return ("Connected")


@app.route('/allGraph')
# Line-Graph showing the occupancy of all libraries in the last ~Day
def itemsGraph(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getAllCurrent()


@app.route('/currentBar')
# Shows the current occupancy of all libraries as Bar-Graph
def currentbar(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return horBar()


@app.route('/currentAvg')
# Shows the average occupancy of all libraries in the last hours as line-graph
def currentavg(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getAverageHalfDay()

@app.route('/avgWkDayAll')
# Shows the average occupancy of all libraries per Weekday (all time)
def avgWeekdayAll(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return avergagebyWeekday()

@app.route('/avgWkDayAllLastTwoWeeks')
# Shows the average occupancy of all libraries per Weekday (last two weeks)
def avgWkDayAllLastTwoWeeks(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return avergagebyWeekdayLastTwoWeeks()

@app.route('/wkdayBib/<string:name>', methods=['GET'])
# Shows the average occupancy of one library per Weekday (all time)
def avgWeekdayBib(self, name):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return avgbyWkdayByBib(name)

@app.route('/wkdayBibLastTwoWeeks/<string:name>', methods=['GET'])
# Shows the average occupancy of one library per Weekday (last two weeks)
def wkdayBibLastTwoWeeks(self, name):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return avgbyWkdayByBibLastTwoWeeks(name)

@app.route('/status')
# Lists the latest scraped entries
def itemsStatus(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    self.setHeader('Content-Type', 'application/json')
    return json.dumps(getCurrentStatus(), default=str)

@app.route('/bib/<string:name>/<string:limit>', methods=['GET'])
# Line-Graph of occupancy by library [name] in the last [limit] entries
def get_item(self, name, limit):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getSingleBib(name, limit)
