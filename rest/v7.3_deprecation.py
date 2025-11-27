from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# --------------------------------------
# Books v1 (old)
# --------------------------------------
books_v1 = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
]

# --------------------------------------
# Books v2 (new)
# --------------------------------------
books_v2 = [
    {"id": 1, "title": "1984", "author": "George Orwell", "published_year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960},
]

DEPRECATION_WARNING = '299 - "API v1 is no longer supported. Please migrate to /api/v2"'

# --------------------------------------
# API v1 — Deprecated
# --------------------------------------
@app.route('/api/v1/books', methods=['GET'])
def get_books_v1():
    resp = make_response({"error": "API v1 is no longer supported. Please migrate to /api/v2"}, 410)
    resp.headers['Warning'] = DEPRECATION_WARNING
    return resp

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book_v1(book_id):
    resp = make_response({"error": "API v1 has been retired. Use /api/v2/books/<id> instead."}, 410)
    resp.headers['Warning'] = DEPRECATION_WARNING
    return resp

@app.route('/api/v1/books', methods=['POST'])
def add_book_v1():
    resp = make_response({"error": "API v1 no longer accepts new data. Switch to /api/v2"}, 410)
    resp.headers['Warning'] = DEPRECATION_WARNING
    return resp

# --------------------------------------
# API v2 — Active
# --------------------------------------
@app.route('/api/v2/books', methods=['GET'])
def get_books_v2():
    return jsonify(books_v2)

@app.route('/api/v2/books/<int:book_id>', methods=['GET'])
def get_book_v2(book_id):
    book = next((b for b in books_v2 if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    return {"error": "Book not found"}, 404

@app.route('/api/v2/books', methods=['POST'])
def add_book_v2():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    data = request.json
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return {"error": "Title and author required"}, 400

    new_id = max(b['id'] for b in books_v2) + 1 if books_v2 else 1

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "published_year": data.get("published_year", 2024)
    }

    books_v2.append(new_book)
    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(port=5003, debug=True)