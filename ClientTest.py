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
    messageQueue.put(message)
    messageReturned[0] = True
    return "Response received"

def acceptMessages():
    serverPort = 8889
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('localhost', serverPort))
    clientSocket.send(input("Please enter phone number to auth from: ").encode())
    clientSocket.close()
    app.run()
    print("Checkpoint")
    #TODO: FIND OUT HOW TO BREAK OUT OF APP AFTER RECEIVING MESSAGE
    #app.do_teardown_appcontext()
    clientSocket.connect(('localhost', serverPort))
    clientSocket.send(messageQueue.get().encode())
    clientSocket.close()
    thread = threading.Thread(target=acceptMessages, daemon=True)
    thread.start()

thread = threading.Thread(target=acceptMessages, daemon=True)
thread.start()
while(True):
    continue
