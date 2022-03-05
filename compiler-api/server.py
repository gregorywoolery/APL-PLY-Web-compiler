import code
from os import error
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from compiler import codeAccept
app = Flask(__name__)
CORS(app)

# API function for reciveing code from client and compiling and returning result.
@app.route("/api/compile", methods=["POST"])
def Compile():
    data = request.get_json()
    compiledTo = codeAccept(data['code'])
    return jsonify(compiledTo)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
