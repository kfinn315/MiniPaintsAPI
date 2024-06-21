
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
    # Extract hex code from the request data
    request_data = json.loads(request.data)
    hex = request_data['hex']

    # Connect to the paint database
    con = sqlite3.connect("paint.db")
    con.text_factory = str
    cursor = con.cursor()

    # Execute the SQL query to retrieve paint colors matching the hex code
    cursor = cursor.execute('SELECT * FROM paint WHERE Hex=?', (hex,))

    # Fetch all matching paint colors
    result = jsonify(message=cursor.fetchall())
    con.close()
    return result


# Helper function to convert a cursor tuple to a dictionary
def tupleToDict(colnames, tuple):
    return {colnames[i]: tuple[i] for i in range(len(tuple))}


@app.route('/api/paint_search', methods=['POST'])
def paint_search():
    # Extract hex code and range from the request data
    request_data = json.loads(request.data)
    hex = request_data['hex']
    range = float(request_data['range'])

    # Connect to the paint database
    con = sqlite3.connect("paint.db")
    con.text_factory = str
    cursor = con.cursor()

    # Execute the SQL query to retrieve all paint colors
    cursor = cursor.execute('SELECT * FROM paint')
    colnames = [description[0] for description in cursor.description]
    paints = cursor.fetchall()
    con.close()

    paint_results = []

    # Iterate over each paint color
    for paint in paints:
        try:
            # Calculate the Delta E value between the given hex code and the paint color
            delta_number = delta_e.delta_e(hex, paint[colnames.index('Hex')])
        except Exception as e:
            # Continue to the next paint color if calculation fails
            continue

        # Check if the Delta E value is within the specified range
        if delta_number < range:
            # Create a dictionary with the paint color and its corresponding Delta E value
            paint_results.append({"paint": tupleToDict(colnames, paint), "delta": roundDeltaE(delta_number)})

    # Return the list of matching paint colors with their Delta E values
    result = jsonify(message=paint_results)
    return result


@app.route('/api/delta', methods=['POST'])
def delta():
    request_data = json.loads(request.data)
    hex1 = request_data['hex1']
    hex2 = request_data['hex2']
    delta_number = delta_e.delta_e(hex1, hex2)
    return jsonify(message=roundDeltaE(delta_number))


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
