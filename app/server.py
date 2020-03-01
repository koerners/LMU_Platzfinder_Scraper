import json
from klein import Klein
from createData import *
from twisted.web.static import File
from createStaticData import reload

app = Klein()
resource = app.resource

@app.route('/')
def items(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return ("Connected")

@app.route('/lastYearAll')
# Get line graph for the average occ in the last 365 day
def getLineLastYear(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getLastYear()

@app.route('/lastYearBib/<string:name>', methods=['GET'])
# Get line graph for the average occ in the last 365 day
def lastYearBib(self, name):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getLastYearBib(name)


@app.route('/wkdayBib/<string:name>', methods=['GET'])
# Shows the average occupancy of one library per Weekday (all time)
def avgWeekdayBib(self, name):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return avgbyWkdayByBib(name)

@app.route('/bibInfo/<string:name>', methods=['GET'])
# Get real name from Bib
def bibInfo(self, name):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return getBibInfo(name)

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


@app.route('/static/', branch=True)
def static(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return File("./static/")

@app.route('/reload')
# Reload the static svgs
def reloadMe(self):
    self.setHeader('Access-Control-Allow-Origin', '*')
    return reload()
