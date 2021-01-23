import slack
import os
import btcprice
from dotenv import load_dotenv
from pathlib import Path
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, Response


# get secrets
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
slack_key = os.getenv("SLACK_BOT_TOKEN")
sign_sec = os.getenv("SIGNING_SECRET")

# flask stuff
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(sign_sec, '/slack/events', app)

# get price
current_price = btcprice.getBitcoinPrice()
print(current_price)

# instantiate bot

client = slack.WebClient(token=slack_key)
BOT_ID = client.api_call("auth.test")['user_id']

# client.chat_postMessage(channel='#bottest', text="Monkey typewriters!")

# @slack_event_adapter.on('message')
# def message(payload):
#     print(payload)
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')
#     # respond with echo
#     if BOT_ID != user_id:
#         client.chat_postMessage(channel=channel_id, text=text)

@app.route('/whoami', methods=['POST'])
def whoami():
    data = request.form
    user_name = data.get('user_name')
    channel_id = data.get('channel_id')
    client.chat_postMessage(channel=channel_id, text=f"{user_name} sent this command")

    return Response(), 200

@app.route('/price', methods=['POST'])
def price():
    data = request.form
    user_name = data.get('user_name')
    channel_id = data.get('channel_id')
    btc_price = current_price

    client.chat_postMessage(
    channel=channel_id, text=f"The current price is: ${btc_price}")

    return Response(), 200


# auto update server and run

if __name__ == "__main__":
    app.run(debug=True)
