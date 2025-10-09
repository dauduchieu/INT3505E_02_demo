from flask import Flask, request, jsonify, make_response
import hashlib, json

app = Flask(__name__)

books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

def generate_etag():
    return hashlib.md5(json.dumps(books, sort_keys=True).encode()).hexdigest()

@app.route('/books', methods=['GET'])
def get_books():
    etag = generate_etag()
    if request.headers.get('If-None-Match') == etag:
        return '', 304
    resp = make_response(jsonify(books))
    resp.headers['Cache-Control'] = 'public, max-age=60'
    resp.headers['ETag'] = etag
    return resp

@app.route('/books', methods=['POST'])
def add_book():
    if not request.is_json:
        return {"error": "JSON only"}, 415
    data = request.get_json()
    title, author = data.get('title'), data.get('author')
    if not title or not author:
        return {"error": "Missing title/author"}, 400
    new_id = max([b['id'] for b in books]) + 1 if books else 1
    new_book = {"id": new_id, "title": title, "author": author}
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)
