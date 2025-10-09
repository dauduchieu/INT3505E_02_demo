from flask import Flask, request, jsonify, make_response
import hashlib
import json

app = Flask(__name__)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

SAMPLE_TOKEN = "hehe123"
def require_token(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {SAMPLE_TOKEN}":
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def generate_etag():
    books_json = json.dumps(books, sort_keys=True)
    return hashlib.md5(books_json.encode()).hexdigest()

@app.route('/books', methods=['GET'])
def get_all_books():
    etag = generate_etag()
    client_etag = request.headers.get('If-None-Match')

    if client_etag == etag:
        return 'Not Modifier', 304

    response = make_response(jsonify(books))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'public, max-age=60'
    response.headers['ETag'] = etag
    return response


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return {"error": "Book not found"}, 404


@app.route('/books', methods=['POST'])
@require_token
def add_book():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    title = request.json.get('title')
    author = request.json.get('author')
    if not title or not author:
        return {"error": "Title and author are required"}, 400

    new_id = max(b["id"] for b in books) + 1 if books else 1
    new_book = {"id": new_id, "title": title, "author": author}

    books.append(new_book)

    response = make_response(jsonify(new_book), 201)
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
