from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

from src.responses import RESPONSES

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    check = body.lower().strip()

    # Start our TwiML response
    resp = MessagingResponse()

    # Check against dictionary
    if RESPONSES.has_key(check):
        resp.messasge(RESPONSES[check])
    elif check == 'test':
        resp.message('Test successful')
    else:
        resp.message("Invalid response, please try again or reply \'START\' to start over")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)