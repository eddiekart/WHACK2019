import threading
import time
import queue
from socket import*

def getMsg(serverSocket):
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=getMsg, args=(serverSocket,), daemon=True)
    thread.start()
    msg = connectionSocket.recv(1024).decode()
    print(msg)
    connectionSocket.send("Bye".encode())
    connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8889))
serverSocket.listen(1)

thread = threading.Thread(target=getMsg, args=(serverSocket,),daemon=True)
thread.start()

while (True):
    continue