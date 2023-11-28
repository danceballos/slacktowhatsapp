"""
import http.client
import json

def lambda_handler(event, context):
    data = json.loads(event['body'])['data'] # Extract data object from the webhook
    message = data['body'] # Message text
    sender = data['from'] # Sender info

    # Prepare the Slack payload
    payload = {
        'text': f'Message from WhatsApp: {message}\nSender: {sender}'
    }
    conn = http.client.HTTPSConnection("hooks.slack.com")
    headers = {'Content-Type': 'application/json'}
    # Send the Slack Message
    conn.request("POST", "/services/T01KCUQ3GQM/B067CCD7JPK/GDsm3cOXEAanxyfKxPZIMAgj", json.dumps(payload), headers)
    response = conn.getresponse()

    print(f'Slack response status: {response.status}, reason: {response.reason}')
    return {
        'statusCode': 200,
        'body': json.dumps('Thanks')
    }
   
    
import http.client
from urllib.parse import urlparse
import json

# Define handler functions for each type
def handle_text(data):
    message = data['body']
    # Process/integrate message text as per your requirements
    return message

def handle_image(data):
    image_url = data['media']
    
    url = urlparse(image_url)
    conn = http.client.HTTPSConnection(url.netloc)
    conn.request("GET", url.path)
    response = conn.getresponse()
    image_file = response.read()

    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    filename = f"{data['body']}.png"  # replace with suitable filename
    headers = {
        "Authorization": "Bearer xoxb-1658976118837-6234856956037-GDCozKFJqGXxtnz242A4IHXu",  # replace with your Bot token
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }

    data = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\nContent-Type: {mimetypes.guess_type(filename)[0]}\r\n\r\n"
    data = data.encode() + image_file + f"\r\n--{boundary}--\r\n".encode()

    conn = http.client.HTTPSConnection("slack.com")

    headers = {
        "Authorization": "Bearer xoxb-your-token",
        "Content-Type": "multipart/form-data; boundary={}".format(boundary),
    }

    payload = (
        "--{}\r\n"
        "Content-Disposition: form-data; name=\"file\"; filename=\"{}\"\r\n"
        "Content-Type: {}\r\n"
        "\r\n"
        "{}\r\n"
        "--{}--\r\n".format(
            boundary, filename, guessed_type, image_file.decode(), boundary
        )
    )
    
    conn.request(
        "POST", "/api/files.upload?channels=target_slack_channel_id", body=payload, headers=headers
    )
    
    response = conn.getresponse()
    return json.loads(response.read())
# Define other handlers...

def lambda_handler(event, context):
    data = json.loads(event['body'])['data']
    sender = data['from']

    handler_map = {
        'text': handle_text,
        'image': handle_image,
    }

    message_type = data['type']
    handler = handler_map.get(message_type)

    if handler:
        payload = handler(data)
        text = data['body'] or "Image received"
    else:
        text = "Unrecognized message type received."
        payload = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            ]
        }

    post_to_slack(text, payload, sender)

def post_to_slack(text, payload, sender):
    blocks = payload.get('blocks', None)  # Returns None if 'blocks' does not exist in payload

    slack_payload = {
        "text": text,
        "blocks": blocks
    }

    print("Final payload:", json.dumps(slack_payload))
    conn = http.client.HTTPSConnection("hooks.slack.com")
    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/services/T01KCUQ3GQM/B067CCD7JPK/GDsm3cOXEAanxyfKxPZIMAgj", json.dumps(slack_payload), headers)
    response = conn.getresponse()
    print(f'Slack response status: {response.status}, reason: {response.reason}')
"""
import http.client
from urllib.parse import urlparse
import json
import mimetypes

def handle_text(data):
    message = data['body']
    return message

def handle_image(data):
    image_url = data['media']

    url = urlparse(image_url)
    conn = http.client.HTTPSConnection(url.netloc)
    conn.request("GET", url.path)
    response = conn.getresponse()
    image_file = response.read() 

    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    filename = f"{data['body']}.png"  # replace with suitable filename

    headers = {
        'Authorization': 'Bearer xoxb-1658976118837-6234856956037-GDCozKFJqGXxtnz242A4IHXu',  # replace with your Bot token
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    }

    # Hard-coding 'image/png' as Content-Type for simplicity:
    payload = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: image/png\r\n'
        f'\r\n'
    ).encode() + image_file + f'\r\n--{boundary}--\r\n'.encode()

    conn = http.client.HTTPSConnection("slack.com")
    conn.request('POST', '/api/files.upload?channels=C066ZL6D5AP', body=payload, headers=headers)

    response = conn.getresponse()
    return json.loads(response.read().decode())


def lambda_handler(event, context):
    data = json.loads(event['body'])['data']
    sender = data['from']

    handler_map = {
        'text': handle_text,
        'image': handle_image,
    }

    message_type = data['type']
    handler = handler_map.get(message_type)

    if handler:
        payload = handler(data)
        text = data['body'] or "Image received"
    else:
        text = "Unrecognized message type received."
        payload = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            ]
        }

    post_to_slack(text, payload, sender)

def post_to_slack(text, payload, sender):
    blocks = payload.get('blocks', None)

    slack_payload = {
        "text": text,
        "blocks": blocks
    }

    print("Final payload:", json.dumps(slack_payload))
    conn = http.client.HTTPSConnection("hooks.slack.com")
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(slack_payload).encode('utf-8')

    conn.request("POST", "/services/T01KCUQ3GQM/B067CCD7JPK/GDsm3cOXEAanxyfKxPZIMAgj", body=payload, headers=headers)
    response = conn.getresponse()

    print(f'Slack response status: {response.status}, reason: {response.reason}')



