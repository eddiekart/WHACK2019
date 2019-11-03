from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from twilio import twiml
import threading
import time

# Array of users
senders = []
firstMessage = True

# SMS Response app
# Message the twilio number that is connected to ngrok, sends a question. Response is accepted, sends right/wrong

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

app.run()
