
import sqlite3
from flask import Flask, jsonify, json, request
from flask_cors import CORS
import delta_e
import numpy

app = Flask(__name__)
CORS(app)

def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)

def roundDeltaE(deltaE):
    return round(deltaE, 2)

@app.route('/api/paint', methods=['POST'])
def paint():
    request_data = json.loads(request.data)
    hex = request_data['hex']
    range = request_data['range']

    # print(hex)
    # print(range)

    con = sqlite3.connect("paint.db")
    con.text_factory = str
    cursor = con.cursor()
    cursor = cursor.execute('SELECT * FROM paint WHERE Hex=?', (hex,))

    result = jsonify(message=cursor.fetchall())
    con.close()
    return result

def tupleToDict(colnames, tuple ):
    return {colnames[i]:tuple[i] for i in range(len(tuple))}

@app.route('/api/paint_search', methods=['POST'])
def paint_search():
    request_data = json.loads(request.data)
    # print(request_data)
    hex = request_data['hex']
    range = float(request_data['range'])

    con = sqlite3.connect("paint.db")
    con.text_factory = str
    cursor = con.cursor()
    cursor = cursor.execute('SELECT * FROM paint')
    colnames = [description[0] for description in cursor.description]
    paints = cursor.fetchall()
    con.close()

    paint_results = []

    for paint in paints:
        try:
            delta_number = delta_e.delta_e(hex, paint[colnames.index('Hex')])
        except Exception as e:
            continue

        if delta_number < range:
            paint_results.append({"paint": tupleToDict(colnames, paint), "delta": roundDeltaE(delta_number)})
    result = jsonify(message=paint_results)
    # print(paint_results)
    return result

@app.route('/api/delta', methods=['POST'])
def delta():
    request_data = json.loads(request.data)
    hex1 = request_data['hex1']
    hex2 = request_data['hex2']
    delta_number = delta_e.delta_e(hex1, hex2)
    return jsonify(message=roundDeltaE(delta_number))


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
