import socket
import sys
import subprocess
import threading


IP = sys.argv[1]
PORT = int(sys.argv[2])

# Sets buffer size to recieve data from server. Max Size.
# Change to what you want.
RECIEVE_SIZE = 4096


# Class for threaded client application.
class ThreadSocketClient(object):

    # Create a socket
    # socket.AF_INET - using IPv4
    # socket.SOCK_STREAM - uses TCP sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Initializes the client application by connecting to the server with IP/PORT defined globally via args.
    def __init__(self):
        self.client_socket.connect((IP, PORT))

        # Creates thread to listen for possible messages/responses from server.
        # using method 'listenToServer' defined within client object.
        listenToServerThread = threading.Thread(target=self.listenToServer, args=(), daemon=True)
        listenToServerThread.start()

        print("connected and listening to server.")

    # method to listen for messages from server.
    # used when creating new connection
    def listenToServer(self):
        while True:
            messageToGet = self.client_socket.recv(RECIEVE_SIZE)
            if messageToGet == b'':
                self.client_socket.close()
                print("Server closed")
                sys.exit()
            else:
                print("Server said: " + messageToGet.decode('utf-8') + "\n>", flush=True)


# Main Program
if __name__ == "__main__":
    # Creates client opject that listens to server and creates sockets.
    client = ThreadSocketClient()

    # Main loop -> send data to server.
    while True:
        messageToSend = input(">")
        if messageToSend == "exitprogram":
            # if client types 'exitprogram' -> closes connection and ends program.
            client.client_socket.close()
            print("Disconnected from Server - closing program")
            sys.exit()
        else:
            # Send data encoded with 'utf-8' that the server can read.
            client.client_socket.send(messageToSend.encode('utf-8'))