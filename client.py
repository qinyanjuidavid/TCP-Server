import socket

header = 64
port = 8080
disconnect_message = "!DISCONNECT"
# server = "192.168.43.170"
server = "127.0.0.1"
address = (server, port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)


def send(msg):
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (header - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode("utf-8"))


send("Hello...")
