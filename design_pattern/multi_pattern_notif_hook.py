from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    data = request.json
    print("Recieve webhook:", data)
    # trigger notification
    print("Send notification to user")
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(port=6000, debug=True)
