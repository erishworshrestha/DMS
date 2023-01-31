import socket
import time
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
clientSocket.connect(("192.168.1.188",80));

data = "toggle";
# clientSocket.send(data.encode())
while True:
#     if(data == "0"):
#         data = "1"
#     elif(data == "1"):
#         data = "0"

    clientSocket.send(data.encode())
    time.sleep(1)
