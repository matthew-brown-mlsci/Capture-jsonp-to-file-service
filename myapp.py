"""

Flask piece of the JSONP capture service

"""

from flask import Flask, jsonify
from flask import request
import sys
import time
import datetime

capture_file = "C:\\scripts\\Capture-jsonp-to-file-service\\data.txt"
app = Flask(__name__)

@app.route("/")
def capture():
    try:
        data = request.args.get('data')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        f = open(capture_file,"a")
        f.write("data|" + data + "|timestamp|" + str(st) + "\n")
        f.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, exception=str(e))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9123)