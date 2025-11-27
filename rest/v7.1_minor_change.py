from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# ---------------------------
# Books v1 (original)
# ---------------------------
books_v1 = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
]

# ---------------------------
# Books v2 (add new optional field: published_year)
# ---------------------------
books_v2 = [
    {"id": 1, "title": "1984", "author": "George Orwell", "published_year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960},
]

# ---------------------------
# v2 API – Optional New Field
# If client does not send published_year → default = current year
# ---------------------------
@app.route('/api/v2/books', methods=['GET'])
def get_books_v2():
    return jsonify(books_v2)

@app.route('/api/v2/books', methods=['POST'])
def add_book_v2():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    body = request.json
    title = body.get('title')
    author = body.get('author')

    if not title or not author:
        return {"error": "Title and author are required"}, 400

    new_id = max(b['id'] for b in books_v2) + 1 if books_v2 else 1

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,

        # Optional field (not required)
        # If not provided → default = current year
        "published_year": body.get('published_year', datetime.datetime.now().year)
    }

    books_v2.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)
