import select, socket, sys, Queue
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 50000))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    print(readable, writable, exceptional)
    
    for s in readable:
        # readable socket has two types:
        # 1. build new connection 
        # 2. accept new message from old connection
        if s is server:
            # new client has arrived
            connection, client_address = s.accept()
            connection.setblocking(0) # non_blocking
            inputs.append(connection)
            message_queues[connection] = Queue.Queue() # current connection will accept many message
        else:
            # some messages have arrived and ready to be read
            data = s.recv(1024)
            if data:
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s) # there are messages can write back
            else: #  no data, disconnect
                if s in outputs:
                    outputs.remove(s)

                inputs.remove(s)
                s.close()

                del message_queues[s] # one connection, multi message

    for s in writable:
        # send message to client
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]