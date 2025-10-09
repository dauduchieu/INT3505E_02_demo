from flask import Flask, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

next_id = 3

@app.route('/', methods=['GET'])
def get_books():
    return books

@app.route('/post-book', methods=['POST'])
def post_book():
    global next_id
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    title = request.json.get('title')
    author = request.json.get('author')
    if not title or not author:
        return {"error": "Title and author are required"}, 400
    new_book = {
        "id": next_id,
        "title": title,
        "author": author
    }
    books.append(new_book)
    next_id += 1
    return new_book, 201

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    

