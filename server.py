import socket
import threading


number_of_clients = 10

header = 64
# port
port = 8078
# pick a server
server = socket.gethostbyname(socket.gethostname())
# address = (server, port)  # ("localhost",8078)
# address = ("localhost", 8078)
# address = ("0.0.0.0", port)
address = ("127.0.0.1", port)
# change the server to listen on either 0.0.0.0

# print(server)

# open a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind my address to the socket
sock.bind(address)

# start the server
print("Server is starting... %s:%s" % (server, port))

client_ranks = []


def start():
    sock.listen(number_of_clients)
    # Wait for a connection
    print("Waiting for a connection...")
    connection, client_address = sock.accept()

    # create a new thread for the client
    client_thread = threading.Thread(
        target=handle_client, args=(connection, client_address)
    )
    client_thread.start()
    print(f"Active connections: {threading.activeCount() - 1}")


def handle_command(connection, rank, command):
    # Only allow clients with lower rank to execute commands from higher rank clients
    if rank < int(command.split()[1]):
        connection.send("Command rejected".encode())
    else:
        connection.send("Command executed".encode())
        print("Client {} executed command: {}".format(rank, command))


def handle_client(connection, address):
    print(f"New connection: {address}")
    # rank connection
    rank = len(client_ranks)
    client_ranks.append(rank)
    connection.append(connection)  # add connection to list of connections
    # Send the client their rank
    connection.send(str(rank).encode())  # client/also connection

    connected = True
    while connected:
        # receive data from the client ,with number of bytes, encode msg to bytes
        data = connection.recv(header).decode("utf-8")
        # if data is a command, handle it
        if data.startswith("command"):
            handle_command(connection, rank, data)

        # If the data is 'disconnect', close the client's socket and remove it from the lists
        elif data == "disconnect":
            connection.close()
            client_ranks.remove(rank)
            connection.remove(connection)
            print("Client {} disconnected".format(rank))

            # Re-adjust the ranks and promote all the clients below the disconnected client
            for i in range(rank, len(client_ranks)):
                client_ranks[i] -= 1
                connection[i].send(str(client_ranks[i]).encode())
            connected = False

        # break


# def handle_client(connection, address):
#     print(f"New connection: {address}")
#     connected = True

#     while connected:
#         # receive data from the client ,with number of bytes, encode msg to bytes
#         msg_length = connection.recv(header).decode("utf-8")
#         # convert to int
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = connection.recv(msg_length).decode("utf-8")
#             # if msg is not empty
#             if msg:
#                 print(f"{address} {msg}")
#                 # send msg back to client
#                 connection.send("Msg received".encode("utf-8"))
#             else:
#                 connected = False

start()
