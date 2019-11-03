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

#Used with ClientTest.py

def processRequest(serverSocket):
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=processRequest, args=(serverSocket,), daemon=True)
    thread.start()
    while True:
        print("Waiting for msg")
        recvMsg = connectionSocket.recv(1024).decode()
        print(recvMsg)
        print(recvMsg[0:1])
        print(recvMsg[0:4])
        print(recvMsg[0:5])
        if (recvMsg[0:1] == "+"):
            account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
            auth_token = 'replace when using'
            client = Client(account_sid, auth_token)
            recvMsg.replace("+",'')
            message = client.messages.create(
                body="Please send AUTH to authorize access; anything else to reject.",
                from_='+16179368426',
                to=recvMsg
            )
            print(message.sid)
            print("Message sent")
            toRecv.append({"sender":recvMsg, "time":time.time()})
        elif (recvMsg[0:4] == "auth"):
            print("in first elif")
            toSend = recvMsg.replace("auth+","")
            print(toSend)
            for x in range(0, len(toRecv)):
                print(toRecv[x]["sender"])
                print("+" + toSend)
                if toRecv[x]["sender"] == "+" + toSend:
                    user = toRecv[x]
                    account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
                    auth_token = 'replace when using'
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        body="AUTH ACCEPTED",
                        from_='+16179368426',
                        to=toSend
                    )
                    print(message.sid)
                    toRecv.remove(user)
                    connectionSocket.close()
                    break
        elif (recvMsg[0:5] == "!auth"):
            toSend = recvMsg.replace("!auth+", "")
            for x in range(0, len(toRecv)):
                if toRecv[x]["sender"] == "+" + toSend:
                    user = toRecv[x]
                    account_sid = 'ACe63a7e0c309b6f39f14c3763b82e7d7a'
                    auth_token = 'replace when using'
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                        body="AUTH REJECTED",
                        from_='+16179368426',
                        to=toSend
                    )
                    print(message.sid)
                    toRecv.remove(user)
                    connectionSocket.close()
                    break
serverPort = 8889
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(9999)

recvReq = threading.Thread(target=processRequest, args=(serverSocket,), daemon=True)
recvReq.start()

print("Threading started")
while (True):
    continue
