from flask import Flask, request
import requests
import os

app = Flask(__name__)
VERIFY_TOKEN = "Test123-Test123-Test123-Test123"
PAGE_ACCESS_TOKEN = "EAAKZA3qSPO0oBO77NXnHAVEETgCmDMexh7ApY0eZBVa6FjYgPYHZCaGF8Cum7eipcj4DrfGvVy8LBZCYr5e4u9URgvLPeeGjMnhGx4M8BUYVtvwcXf8xwZBCZBU9V3il6SZACxcaZBnn8cBOaaq2REWfmRxkK2L7edExaCsDF8rDcKFthQ91hoZCM1LtADcIp1HDCZC3gbP24ZD"


@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            if messaging_event.get('message'):
                sender_id = messaging_event['sender']['id']
                message_text = messaging_event['message']['text']
                send_message(sender_id, f"You said: {message_text}")
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v12.0/me/messages",
                  params=params, headers=headers, json=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
