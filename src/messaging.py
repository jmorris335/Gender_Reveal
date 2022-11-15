from twilio.rest import Client

from src.secrets import *

# Find your Account SID and Auth Token in Account Info and set the environment variables.
# See http://twil.io/secure

class Messages:
    def __init__(self):
        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.number = TWILIO_NUMBER
        self.client = Client(self.account_sid, self.auth_token)

    def sendMessage(self, body='Test Message', to_num='+18018503126'):
        message = self.client.messages.create(
            body=body,
            from_=self.number,
            to=to_num
        )
        print(message.status)
