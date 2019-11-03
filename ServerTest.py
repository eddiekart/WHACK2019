from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import threading
import time
import queue
from socket import*

senders = []
authNum = []
toRecv = []

def processRequest(serverSocket):
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=processRequest, args=(serverSocket,), daemon=True)
    thread.start()
    recvMsg = connectionSocket.recv(1024).decode()
    print(recvMsg)
    if (recvMsg[0] == '+'):
        account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
        auth_token = '50a7249b40eb3857667e7114722d734e'
        client = Client(account_sid, auth_token)
        recvMsg.replace("+",'')
        message = client.messages.create(
            body="Please send AUTH to authorize access; anything else to reject.",
            from_='+16179368426',
            to='7817083718'
        )
        print(message.sid)
        print("Message sent")
        toRecv.append({"sender":recvMsg, "time":time.time()})
    elif (recvMsg[0:5] == "AUTH"):
        recvMsg.replace("AUTH+","")
        for x in range(0, len(toRecv)):
            if toRecv[x]["sender"] is recvMsg:
                user = toRecv[x]["sender"]
                account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
                auth_token = '50a7249b40eb3857667e7114722d734e'
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body="AUTH REJECTED",
                    from_='+16179368426',
                    to=user["sender"]
                )
                print(message.sid)
                recvMsg.remove(user)
    elif (recvMsg[0:6] == "!AUTH"):
        recvMsg.replace("!AUTH+","")
        for x in range(0, len(toRecv)):
            if toRecv[x]["sender"] is recvMsg:
                user = toRecv[x]["sender"]
                account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
                auth_token = '50a7249b40eb3857667e7114722d734e'
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body="AUTH REJECTED",
                    from_='+16179368426',
                    to=user["sender"]
                )
                print(message.sid)
                recvMsg.remove(user)
serverPort = 8889
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(9999)

recvReq = threading.Thread(target=processRequest, args=(serverSocket,), daemon=True)
recvReq.start()

print("Threading started")
while (True):
    continue
