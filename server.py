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
        for row in c.execute('SELECT * FROM `auslastung`'):
            self._items.append(row)
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)

    @app.route('/bib/<string:name>/<string:limit>', methods=['GET'])
    def get_item(self, request, name, limit):
        self._items.clear();
        fields = [name, limit]
        for row in c.execute('SELECT * FROM `auslastung` where Ort = ? order by PK desc limit ?', fields):
            self._items.append(row)
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)


if __name__ == '__main__':
    store = ItemStore()
    store.app.run('', 8080)
