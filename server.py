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
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)


    @app.route('/var/<string:name>', methods=['GET'])
    def get_item(self, request, name):
        return name


if __name__ == '__main__':
    store = ItemStore()
    store.app.run('', 8080)
