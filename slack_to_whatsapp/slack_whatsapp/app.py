import json
import http.client

def send_message_to_whatsapp(recipient, message):
    con = http.client.HTTPSConnection("api.ultramsg.com")
    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "token": "s9d4cuporszzoo4t",
        "to": recipient,
        "body": message
    })

    con.request("POST", "/instance69430/messages/chat", body=payload, headers=headers)
    response = con.getresponse()

    print(response.read().decode())

def lambda_handler(event, context):
    slack_event = json.loads(event['body'])
    # Respond to Slack challenge
    if 'type' in slack_event and slack_event['type'] == 'url_verification':
        # Respond to the challenge
        return {
            'statusCode': 200,
            'body': slack_event['challenge']
        }
    if 'subtype' in slack_event['event'] and slack_event['event']['subtype'] == 'bot_message':
        # Ignore bot messages
        return {
            'statusCode': 200,
            'body': json.dumps('Ignored bot message')
        }

    # Remaining message is considered as user message
    slack_message = slack_event['event']['text']
    slack_user = slack_event['event']['user']
    whatsapp_user = "120363201004742031@g.us"  # replace with appropriate logic for user mapping

    # Send message to WhatsApp
    send_message_to_whatsapp(whatsapp_user, slack_message)

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent')
    }
