# messaging/twilio_utils.py
from twilio.rest import Client

# Initialize Twilio client with your credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)


# Function to send a message
def send_message(to_number, message_body):
    message = client.messages.create(
        body=message_body,
        from_='your_twilio_phone_number',
        to=to_number
    )
    return message.sid
