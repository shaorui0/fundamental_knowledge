import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))
print(s)
while True:
    s.sendall('Hello, world')
    data = s.recv(1024)
    print 'Received', repr(data)
    import time 
    time.sleep(1)
s.close()
