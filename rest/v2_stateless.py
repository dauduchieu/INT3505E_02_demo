from flask import Flask, request

app = Flask(__name__)
books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee"
    }
]

@app.route('/books', methods=['GET'])
def get_all_books():
    return books

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        return book
    return {"error": "Book not found"}, 404

SAMPLE_TOKEN = "hehe123"
def require_token(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {SAMPLE_TOKEN}":
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/books', methods=['POST'])
@require_token
def add_book():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    title = request.json.get('title')
    author = request.json.get('author')
    if not title or not author:
        return {"error": "Title and author are required"}, 400
    new_id = max(book["id"] for book in books) + 1 if books else 1
    new_book = {
        "id": new_id,
        "title": title,
        "author": author
    }
    books.append(new_book)
    return new_book, 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
