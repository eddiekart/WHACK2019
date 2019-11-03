from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from twilio import twiml
import threading
import time

# Array of users
senders = []
firstMessage = True

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    timeout = 20
    # Removes timed out users; times out 20 seconds after initial connect
    for x in range(0, len(senders)):
        if (time.time() - senders[x]["startTime"]) > timeout:
            senders.remove(senders[x])

    # Sets up sender/msg/response variables
    sender = request.values.get('From')
    msg = request.values.get('Body').lower().strip()
    print("Sender: " + sender)
    print("Message: " + msg)
    resp = MessagingResponse()

    # Checks if this number previously sent a msg
    userFound = False
    for x in range(0, len(senders)):
        user = senders[x]
        if sender == user["sender"]:
            userFound = True
            # If found, checks msg to see if it's correct response to msg initially sent
            if msg == '2':
                message = "Correct!!!!"
            else:
                message = "Wrong!"
            # Removes user from user list to reset state
            senders.remove(user)

    # If this is the first time user is contacting (or 1st time after answering Q), stores data in server
    if (not userFound):
        # Makes dictionary w/ sender #, time sent into database
        senders.append({"sender": sender, "startTime": time.time()})
        message = "What is 1+1? Answer within " + str(timeout) + " seconds."
    print("Response: " + message)
    resp.message(message)
    return str(resp)

app2 = Flask(__name__)

@app2.route('/sms', methods=['GET','POST'])
def sms2():
    sender = request.values.get('From')
    print(sender)
    resp = MessagingResponse()
    resp.message("SMS2!!!")
    return str(resp)

#if __name__ == "__main__":
if (firstMessage):
    app2.run(debug=True)
    firstMessage = False
else :
    app.run(debug=True)
