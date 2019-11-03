from socket import*
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import threading
import time
import queue
from socket import*


messageQueue = queue.Queue()
messageReturned = [False]
cont = []
cont.append(False)

# used with ServerTest.py
# Input: a phone number to send AUTH message to. Interaction is between number and Twilio # connected to ngrok

app = Flask(__name__)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if (messageReturned[0]):
        app.do_teardown_appcontext()
    sender = request.values.get('From')
    msg = request.values.get('Body').lower().strip()
    print("Sender: " + sender)
    print("Message: " + msg)
    resp = MessagingResponse()
    message = ''
    if msg == "auth":
        message = "auth" + sender
    else:
        message = "!auth" + sender
    print(message)
    print("I got here")
    messageQueue.put(message)
    cont[0] = True
    print("I got here")
    messageReturned[0] = True
    print("I got here")
    resp.message("Response received")
    return str(resp)

def acceptMessages():
    serverPort = 8889
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('localhost', serverPort))
    clientSocket.send(input("Please enter phone number to auth from: ").encode())
    print("Checkpoint")
    #TODO: FIND OUT HOW TO BREAK OUT OF APP AFTER RECEIVING MESSAGE
    #app.do_teardown_appcontext()
    while (True):
        if (cont[0]):
            print("in cont")
            clientSocket.send(messageQueue.get().encode())
            print("msg sent")
            clientSocket.close()
            cont[0] = False
            thread = threading.Thread(target=acceptMessages,daemon=True)
            thread.start()
            break
        else:
            continue


thread = threading.Thread(target=acceptMessages, daemon=True)
thread.start()
app.run()
while(True):
    continue
