# ========== URL versioning ============
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/books', methods=['GET'])
def books_v1():
    return jsonify({"version": "v1", "data": ["Book A", "Book B"]})

@app.route('/api/v2/books', methods=['GET'])
def books_v2():
    return jsonify({"version": "v2", "data": ["Book A", "Book B", "Book C"]})

if __name__ == "__main__":
    app.run(port=5001)


# ========== Header versioning ============
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/books', methods=['GET'])
def books_header_version():
    version = request.headers.get("X-API-Version", "1")

    if version == "1":
        return jsonify({"version": "v1", "data": ["Book A", "Book B"]})
    elif version == "2":
        return jsonify({"version": "v2", "data": ["Book A", "Book B", "Book C"]})
    return jsonify({"error": "Unsupported API version"}), 400

if __name__ == "__main__":
    app.run(port=5002)
    
    
# ============ Query versioning ============
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/books', methods=['GET'])
def books_query_version():
    version = request.args.get("version", "1")

    if version == "1":
        return jsonify({"version": "v1", "data": ["Book A", "Book B"]})
    elif version == "2":
        return jsonify({"version": "v2", "data": ["Book A", "Book B", "Book C"]})
    return jsonify({"error": "Unsupported API version"}), 400

if __name__ == "__main__":
    app.run(port=5003)

