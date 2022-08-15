import slack
import os
import requests
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Path to the .env file which contains static data
# . Represents current directory and load the file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Handle POST requests 
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'] , '/slack/events', app)

# We make use of Slack Web API for this application, which needs an authentication token
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

# Function to check if the value lies between 0 to 255, which is required for IP identication
def isIPv4(s):
    try: return str(int(s)) == s and 0 <= int(s) <= 255
    except: return False

#function to handle message events
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    # Using Regex to eliminate all alphabets and all outlier numbers
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    text = pattern.search(text)[0]

    # URL headers to query VirusTotal API
    url = os.environ['URL'] + text
    headers = {
    "Accept": "application/json",
    "x-apikey": os.environ['APIKEY']
    }

    # Using response variable to store the JSON information from the VirusTotal API
    response = requests.get(url, headers=headers)
    json_object = json.loads(response.text)

    # IFcondition to make sure outlier IPs do not pass. eg - 360.180.23.21
    if text.count(".") == 3 and all(isIPv4(i) for i in text.split(".")):
        ipnet = "Network is " + json_object["data"]["attributes"]["network"] + "\n Country is " + json_object["data"]["attributes"]["country"] + "\n Owner is " + json_object["data"]["attributes"]["as_owner"] + "\n Harmless percentage " + str(json_object["data"]["attributes"]["last_analysis_stats"]["harmless"])
    else:
        ipnet = ""
    
    # Bot reads all messages, to make sure that bot does not read its own message and create a loop, a comparison is made with the user id and bot id
    # Bot uses chat_postMessage to post messages on the channel
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=ipnet)

# Run flask application on default port 5000
# Add argument "port = 8000" to change it to 8000 in app.run
if __name__ == "__main__":
    app.run(debug=True)