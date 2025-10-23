from flask import Flask, request, jsonify, make_response
import hashlib
import json

app = Flask(__name__)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 4, "title": "Brave New World", "author": "Aldous Huxley"},
    {"id": 5, "title": "Fahrenheit 451", "author": "Ray Bradbury"},
    {"id": 6, "title": "Animal Farm", "author": "George Orwell"},
    {"id": 7, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 8, "title": "Lord of the Flies", "author": "William Golding"},
    {"id": 9, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 10, "title": "Moby Dick", "author": "Herman Melville"},
    {"id": 11, "title": "War and Peace", "author": "Leo Tolstoy"},
    {"id": 12, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    {"id": 13, "title": "The Odyssey", "author": "Homer"},
    {"id": 14, "title": "Ulysses", "author": "James Joyce"},
    {"id": 15, "title": "The Divine Comedy", "author": "Dante Alighieri"}
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


def generate_etag(data_books=None):
    if data_books is None:
        data_books = books
    books_json = json.dumps(data_books, sort_keys=True)
    return hashlib.md5(books_json.encode()).hexdigest()

@app.route('/books', methods=['GET'])
def get_all_books():
    # Page-based pagination
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 2))
    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(books) + limit - 1) // limit
    paged_books = books[start:end]
    
    etag = generate_etag(data_books=paged_books)
    client_etag = request.headers.get('If-None-Match')

    if client_etag == etag:
        return 'Not Modifier', 304
    
    data = {
        "page": page,
        "total_pages": total_pages,
        "results": paged_books
    }

    response = make_response(jsonify(data))
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
    
