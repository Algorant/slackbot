import slack
import os
from dotenv import load_dotenv
from pathlib import Path
from slackeventsapi import SlackEventAdapter
from flask import Flask


# get secrets
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
slack_key = os.getenv("SLACK_BOT_TOKEN")
sign_sec = os.getenv("SIGNING_SECRET")

# flask stuff
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(sign_sec, '/slack/events', app)


# instantiate bot

client = slack.WebClient(token=slack_key)
BOT_ID = client.api_call("auth.test")['user_id']

# client.chat_postMessage(channel='#bottest', text="Monkey typewriters!")

@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    # respond with echo
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text="text")




# auto update server and run

if __name__ == "__main__":
    app.run(debug=True)
