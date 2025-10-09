from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
SERVICE_URL = "http://127.0.0.1:5001"

SAMPLE_TOKEN = "hehe123"

@app.before_request
def check_auth():
    if request.method == "POST":
        token = request.headers.get('Authorization')
        if token != f"Bearer {SAMPLE_TOKEN}":
            return {"error": "Unauthorized"}, 401

@app.route('/books', methods=['GET', 'POST'])
def proxy_books():
    url = f"{SERVICE_URL}/books"

    if request.method == 'GET':
        headers = {k: v for k, v in request.headers if k.lower().startswith('if-')}
        resp = requests.get(url, headers=headers)
        return (resp.text, resp.status_code, resp.headers.items())

    if request.method == 'POST':
        resp = requests.post(url, json=request.json)
        return (resp.text, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
