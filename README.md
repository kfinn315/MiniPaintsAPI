# Mini Paints API

This code is a Flask application that operates as a RESTful API for a paint database. It allows users to search for paint colors based on a given hex code and range of color difference, as well as calculate the color difference between two hex codes.

The code begins by importing the necessary dependencies: sqlite3 for database operations, Flask for creating the API, jsonify and json for JSON responses, and Flask-CORS for enabling cross-origin resource sharing.

It defines a Flask application and enables CORS for handling cross-origin requests.

A helper function patch_asscalar is defined to handle converting numpy arrays to scalars for compatibility.

Another helper function roundDeltaE is defined to round Delta E values to two decimal places.

The code also defines a helper function tupleToDict to convert a cursor tuple result to a dictionary with column names as keys.

Finally, the code runs the Flask application on host 0.0.0.0 and port 5000 when executed directly.


## Usage
The API has three endpoints:

/api/paint - Accepts a POST request with a JSON body containing a hex code (hex) and a range (range). It retrieves paint colors from a SQLite database (paint.db) that match the given hex code. The response is a JSON message containing the matched paint colors.

/api/paint_search - Accepts a POST request with a JSON body containing a hex code (hex) and a range (range). It retrieves all paint colors from the database and calculates the Delta E value between the given hex code and each paint color. If the Delta E value is within the specified range, the paint color is added to the response. The response is a JSON message containing the matched paint colors and their Delta E values.

/api/delta - Accepts a POST request with a JSON body containing two hex codes (hex1 and hex2). It calculates the Delta E value between the two hex codes and returns it as a JSON message.


## Installation
To run the code, make sure you have the necessary dependencies installed, and then execute the script in your Python environment.
