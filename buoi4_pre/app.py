from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake database in memory
books = []
borrows = []
book_id_counter = 1
borrow_id_counter = 1

# ------------------- BOOKS -------------------
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({"data": books}), 200

@app.route("/books", methods=["POST"])
def add_book():
    global book_id_counter
    data = request.json
    if not data.get("title") or not data.get("author"):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields",
            "details": [{"field": "title"}, {"field": "author"}],
            "hint": "Provide 'title' and 'author'"
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

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    return jsonify(book), 200

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    
    data = request.json
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    return jsonify(book), 200

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({}), 204

# ------------------- BORROWS -------------------
@app.route("/borrows", methods=["POST"])
def borrow_book():
    global borrow_id_counter
    data = request.json
    book_id = data.get("book_id")

    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"code": "NOT_FOUND", "message": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"code": "CONFLICT", "message": "Book is already borrowed"}), 409

    book["available"] = False
    borrow = {
        "id": borrow_id_counter,
        "book_id": book_id,
        "returned": False
    }
    borrows.append(borrow)
    borrow_id_counter += 1
    return jsonify(borrow), 201

@app.route("/borrows/<int:borrow_id>/return", methods=["PUT"])
def return_book(borrow_id):
    borrow = next((br for br in borrows if br["id"] == borrow_id), None)
    if not borrow:
        return jsonify({"code": "NOT_FOUND", "message": "Borrow record not found"}), 404
    if borrow["returned"]:
        return jsonify({"code": "CONFLICT", "message": "Book already returned"}), 409

    borrow["returned"] = True
    book = next((b for b in books if b["id"] == borrow["book_id"]), None)
    if book:
        book["available"] = True
    return jsonify(borrow), 200

# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)
