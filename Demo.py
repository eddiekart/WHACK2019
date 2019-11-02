from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from twilio import twiml


app = Flask(__name__)
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    msg = request.values.get('Body').lower().strip()
    resp = MessagingResponse()
    print(msg)
    if msg == "matcha":
        resp.message("noice")
    elif msg == "eddie is babo":
        resp.message("No christina is super babo")
    else:
        resp.message("meh")
    #resp.message("THANK YOU FOR MESSAGING ME!!!!")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


