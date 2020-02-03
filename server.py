import json
from klein import Klein
import sqlite3

conn = sqlite3.connect('bib.db')
c = conn.cursor()


class ItemStore(object):
    app = Klein()

    def __init__(self):
        self._items = []

    @app.route('/')
    def items(self, request):
        self._items.clear()
        for row in c.execute('SELECT * FROM `auslastung` order by PK desc limit 200'):
            self._items.append(row)
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)

    @app.route('/bib/<string:name>/<string:limit>', methods=['GET'])
    def get_item(self, request, name, limit):
        self._items.clear()
        fields = [name, limit]
        for row in c.execute('SELECT * FROM `auslastung` where Ort = ? order by PK desc limit ?', fields):
            self._items.append(row)
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)


if __name__ == '__main__':
    store = ItemStore()
    store.app.run('', 8080)
