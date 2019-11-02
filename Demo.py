from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from twilio import twiml
import threading
import time

waitingForAnswer = [1]
waitingForAnswer[0] = False
start = [1]
start[0] = time.time()
end = [1]
end[0] = time.time()

senders = []

app = Flask(__name__)
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    #Removes timed out users
    print(len(senders))
    for x in range(0, len(senders)):
        if (time.time() - senders[x]["startTime"]) > 10:
            senders.remove(senders[x])
    print(len(senders))

    #Sets up sender/msg/response variables
    sender = request.values.get('From')
    msg = request.values.get('Body').lower().strip()
    resp = MessagingResponse()

    #Checks if this number previously sent a msg
    userFound = False
    for x in range(0, len(senders)):
        user = senders[x]
        if sender == user["sender"]:
            userFound = True
            #If found, checks msg to see if it's correct response to msg initially sent
            if msg == '2':
                print("in msg == 2")
                message = "Correct!!!!"
            else:
                print("in else")
                message = "Wrong!"
            print("In if, after ifelse")
            #Removes user from user list to reset state
            senders.remove(user)

    #If this is the first time user is contacting (or 1st time after answering Q), stores data in server
    if (not userFound):
        #Makes dictionary w/ sender #, time sent into database
        senders.append({"sender": sender, "startTime": time.time()})
        print("In else outer")
        message = "What is 1+1? Answer within 10 seconds."
    resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)




