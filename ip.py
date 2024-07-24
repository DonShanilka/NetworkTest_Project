import socket

hostname = socket.gethostname()
myip = socket.gethostbyname(hostname)
print("My ip address is " + myip)