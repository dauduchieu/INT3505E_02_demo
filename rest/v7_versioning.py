from flask import Flask, request, jsonify, make_response
import hashlib
import json
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_jwt_key'
token_expiration_seconds = 3600

users = [
    {"id": 1, "username": "admin", "password": "123", "role": "admin"},
    {"id": 2, "username": "user", "password": "123", "role": "user"}
]

# ---------------------------
# Versioned books
# ---------------------------
books_v1 = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 4, "title": "Brave New World", "author": "Aldous Huxley"},
]

books_v2 = [
    {"id": 1, "title": "1984", "author": "George Orwell", "published_year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien", "published_year": 1937},
    {"id": 4, "title": "Brave New World", "author": "Aldous Huxley", "published_year": 1932},
]

# Warning header for deprecated API v1
DEPRECATION_WARNING = '299 - "API v1 will be deprecated on 2025-12-31"'

# ---------------------------
# JWT helpers
# ---------------------------
def generate_token(user):
    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=token_expiration_seconds)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def require_token(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or not token.startswith("Bearer "):
                return {"error": "Unauthorized"}, 401
            token = token.split(" ")[1]
            decoded = decode_token(token)
            if "error" in decoded:
                return decoded, 401
            if role and decoded.get('role') != role:
                return {"error": "Forbidden"}, 403
            request.user = decoded
            return f(*args, **kwargs)
        return wrapper
    return decorator

def generate_etag(data_books=None):
    if data_books is None:
        data_books = []
    books_json = json.dumps(data_books, sort_keys=True)
    return hashlib.md5(books_json.encode()).hexdigest()

# ---------------------------
# Authentication
# ---------------------------
@app.route('/api/<version>/login', methods=['POST'])
def login(version):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    username = request.json.get('username')
    password = request.json.get('password')
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if not user:
        return {"error": "Invalid credentials"}, 401
    token = generate_token(user)
    return jsonify({
        "token": token,
        "token_type": "Bearer",
        "expires_in": token_expiration_seconds
    })

# ---------------------------
# Generic helpers
# ---------------------------
def get_books_generic(book_list, deprecated=False):
    search = request.args.get('search', '').lower()
    filtered_books = [b for b in book_list if search in b['title'].lower() or search in b['author'].lower()] if search else book_list
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 2))
    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(filtered_books) + limit - 1) // limit
    paged_books = filtered_books[start:end]

    etag = generate_etag(paged_books)
    client_etag = request.headers.get('If-None-Match')
    if client_etag == etag:
        return 'Not Modified', 304

    data = {"page": page, "total_pages": total_pages, "results": paged_books}
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'public, max-age=60'
    response.headers['ETag'] = etag
    if deprecated:
        response.headers['Warning'] = DEPRECATION_WARNING
    return response

def add_book_generic(book_list):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    title = request.json.get('title')
    author = request.json.get('author')
    if not title or not author:
        return {"error": "Title and author are required"}, 400
    new_id = max(b['id'] for b in book_list) + 1 if book_list else 1
    new_book = {"id": new_id, "title": title, "author": author}
    if book_list is books_v2:
        new_book["published_year"] = request.json.get('published_year', 2025)
    book_list.append(new_book)
    response = make_response(jsonify(new_book), 201)
    return response

# ---------------------------
# Books v1 (deprecated)
# ---------------------------
@app.route('/api/v1/books', methods=['GET'])
# @require_token()
def get_books_v1():
    return get_books_generic(books_v1, deprecated=True)

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
# @require_token()
def get_book_v1(book_id):
    book = next((b for b in books_v1 if b['id'] == book_id), None)
    if book:
        resp = make_response(jsonify(book))
        resp.headers['Warning'] = DEPRECATION_WARNING
        return resp
    resp = make_response(jsonify({"error": "Book not found"}), 404)
    resp.headers['Warning'] = DEPRECATION_WARNING
    return resp

@app.route('/api/v1/books', methods=['POST'])
@require_token(role='admin')
def add_book_v1():
    response = add_book_generic(books_v1)
    response.headers['Warning'] = DEPRECATION_WARNING
    return response

# ---------------------------
# Books v2
# ---------------------------
@app.route('/api/v2/books', methods=['GET'])
@require_token()
def get_books_v2():
    return get_books_generic(books_v2)

@app.route('/api/v2/books/<int:book_id>', methods=['GET'])
@require_token()
def get_book_v2(book_id):
    book = next((b for b in books_v2 if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    return {"error": "Book not found"}, 404

@app.route('/api/v2/books', methods=['POST'])
@require_token(role='admin')
def add_book_v2():
    return add_book_generic(books_v2)

# ---------------------------
# Run server
# ---------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
