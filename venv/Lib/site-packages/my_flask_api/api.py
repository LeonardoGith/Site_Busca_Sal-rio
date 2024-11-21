from . import app
from flask import jsonify

@app.route('/api/v1/hello', method=['GET'])
def hello_world():
    return jsonify({'message' : 'Hello, World!'})

def run():
    app.run(debug=True)