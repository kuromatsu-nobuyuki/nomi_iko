import requests
import json
from user import MATTERMOST_TOKEN, MATTERMOST_SERVER

def make_json_pay_load(message):
    payload = {
        'response_type': "in_channel",
        'text': str(message),
        'MATTERMOST_TOKEN': MATTERMOST_TOKEN
    }
    json_payload = json.dumps(payload)
    return json_payload


def send_message(json=None):
    requests.post(url=MATTERMOST_SERVER ,data=json)

