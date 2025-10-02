from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake in-memory database
books = []
book_id_counter = 1


# ------------------- BOOKS -------------------
@app.route("/books", methods=["GET"])
def get_books():
    """Get list of all books"""
    return jsonify({"data": books}), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get a single book by ID"""
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def add_book():
    """Add a new book"""
    global book_id_counter
    data = request.json

    if not data.get("title") or not data.get("author"):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields",
            "details": [{"field": "title"}, {"field": "author"}]
        }), 400

    new_book = {
        "id": book_id_counter,
        "title": data["title"],
        "author": data["author"],
        "available": True
    }
    books.append(new_book)
    book_id_counter += 1
    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    """Edit a book"""
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404

    data = request.json
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    return jsonify(book), 200


# ------------------- BORROW / RETURN -------------------
@app.route("/books/<int:book_id>/borrow", methods=["PUT"])
def borrow_book(book_id):
    """Borrow a book (mark as unavailable)"""
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"code": "CONFLICT", "message": "Book already borrowed"}), 409

    book["available"] = False
    return jsonify(book), 200


@app.route("/books/<int:book_id>/return", methods=["PUT"])
def return_book(book_id):
    """Return a book (mark as available again)"""
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    if book["available"]:
        return jsonify({"code": "CONFLICT", "message": "Book was not borrowed"}), 409

    book["available"] = True
    return jsonify(book), 200


# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)
