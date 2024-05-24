from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api1', methods=['GET'])
def api1():
    return jsonify({"message": "Response from API 1"})

@app.route('/api2', methods=['GET'])
def api2():
    return jsonify({"message": "Response from API 2"})

if __name__ == '__main__':
    app.run(debug=True)