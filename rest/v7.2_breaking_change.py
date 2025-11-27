from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------------------
# Books v1 (old contract)
# title (string), author (string)
# ---------------------------
books_v1 = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
]

# ---------------------------
# Books v2 (breaking change)
# renamed field:
#   author  → written_by  (breaking)
# removed field:
#   title (replaced with book_title)
# Both are REQUIRED → missing → error
# ---------------------------
books_v2 = [
    {"id": 1, "book_title": "1984", "written_by": "George Orwell"},
    {"id": 2, "book_title": "To Kill a Mockingbird", "written_by": "Harper Lee"},
]

# ---------------------------
# v2 API – Breaking Changes Enforcement
# ---------------------------
@app.route('/api/v2/books', methods=['GET'])
def get_books_v2():
    return jsonify(books_v2)

@app.route('/api/v2/books', methods=['POST'])
def add_book_v2():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    body = request.json

    # Breaking change: v2 requires NEW fields
    book_title = body.get('book_title')
    written_by = body.get('written_by')

    # Missing new required fields → ERROR
    if not book_title or not written_by:
        return {
            "error": "Breaking change: 'book_title' and 'written_by' are required in API v2."
        }, 400

    new_id = max(b['id'] for b in books_v2) + 1 if books_v2 else 1

    new_book = {
        "id": new_id,
        "book_title": book_title,
        "written_by": written_by
    }

    books_v2.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(port=5002, debug=True)