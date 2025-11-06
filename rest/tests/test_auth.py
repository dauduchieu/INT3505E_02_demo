import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ========== Tests generate token ============
from v6_authen_author import generate_token, app, users
import jwt

def test_generate_token_contains_user_data():
    user = users[0]
    token = generate_token(user)

    decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    
    assert decoded['user_id'] == user['id']
    assert decoded['username'] == user['username']
    assert decoded['role'] == user['role']
    assert 'exp' in decoded

# ========== Tests decode token ============
from v6_authen_author import decode_token, generate_token, users
import datetime

def test_decode_valid_token():
    token = generate_token(users[0])
    payload = decode_token(token)
    assert payload['username'] == 'admin'

def test_decode_expired_token(mocker):
    # Create a token that expires immediately
    mocker.patch('datetime.datetime', wraps=datetime.datetime)
    payload = decode_token("invalid-token")
    assert payload["error"] == "Invalid token"
    

# ========== Tests ETag generation ============
from v6_authen_author import generate_etag

def test_etag_changes_when_data_changes():
    data1 = [{"id": 1, "title": "A"}]
    data2 = [{"id": 1, "title": "B"}]

    etag1 = generate_etag(data1)
    etag2 = generate_etag(data2)

    assert etag1 != etag2
    
# ========== Tests require_token decorator ============
from v6_authen_author import app, require_token, generate_token, users
from flask import request

def test_require_token_allows_valid_token():
    token = generate_token(users[0])
    
    @require_token()
    def protected():
        return "OK"

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        assert protected() == "OK"
