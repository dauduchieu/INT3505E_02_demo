from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# =====================================================
# Mock Database
# =====================================================
books = [
    {"id": 1, "title": "Clean Code", "category": "IT", "quantity": 2},
    {"id": 2, "title": "1984", "category": "Novel", "quantity": 0},
    {"id": 3, "title": "The Pragmatic Programmer", "category": "IT", "quantity": 1},
]

# webhook subscribers
subscribers = ["http://localhost:6000/webhook"]


# =====================================================
# CRUD + QUERY PATTERN
# =====================================================
@app.route("/books", methods=["GET"])
def get_books():
    result = books

    # ------ Filtering ------
    category = request.args.get("category")
    if category:
        result = [b for b in result if b["category"].lower() == category.lower()]

    # ------ Pagination ------
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    start = (page - 1) * limit
    end = start + limit
    result = result[start:end]

    # ------ Sorting ------
    sort = request.args.get("sort")  # vd: sort=-id
    if sort:
        field = sort.lstrip("-")
        reverse = sort.startswith("-")
        result = sorted(result, key=lambda x: x[field], reverse=reverse)

    # ------ Field Selection ------
    fields = request.args.get("fields")  # vd: fields=id,title
    if fields:
        field_list = fields.split(",")
        result = [{k: b[k] for k in field_list if k in b} for b in result]

    return jsonify(result)


# =====================================================
# HATEOAS VERSION (Recommended)
# =====================================================
@app.route("/books/hateoas", methods=["GET"])
def get_books_hateoas():
    response = []
    for b in books:
        book_data = dict(b)

        # Thêm HATEOAS links tùy trạng thái
        links = {
            "self": f"/books/{b['id']}",
            "borrow": f"/books/{b['id']}/borrow" if b["quantity"] > 0 else None,
            "return": f"/books/{b['id']}/return",
        }
        book_data["_links"] = links

        response.append(book_data)

    return jsonify(response)


# =====================================================
# Borrow Book (Business Logic + Event Trigger)
# =====================================================
@app.route("/books/<int:book_id>/borrow", methods=["POST"])
def borrow_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return {"error": "Book not found"}, 404

    if book["quantity"] <= 0:
        return {
            "error": "Book out of stock",
            "next_actions": {
                "waitlist": f"/books/{book_id}/waitlist",
                "similar_books": "/books?category=" + book["category"]
            }
        }, 400

    # Borrow thành công
    book["quantity"] -= 1

    # Trigger Webhook Event
    for sub in subscribers:
        try:
            requests.post(sub, json={
                "event": "book.borrowed",
                "book_id": book_id,
                "timestamp": datetime.datetime.now().isoformat()
            })
        except:
            print("Webhook gửi thất bại:", sub)

    return {"message": "Borrowed successfully", "book": book}, 200


# =====================================================
# Return Book
# =====================================================
@app.route("/books/<int:book_id>/return", methods=["POST"])
def return_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return {"error": "Book not found"}, 404

    book["quantity"] += 1

    # Gửi webhook
    for sub in subscribers:
        requests.post(sub, json={
            "event": "book.returned",
            "book_id": book_id,
            "timestamp": datetime.datetime.now().isoformat()
        })

    return {"message": "Returned successfully", "book": book}, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
