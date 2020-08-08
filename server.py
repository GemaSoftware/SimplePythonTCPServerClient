import socket
import threading
import sys
import subprocess

# Gets arguments from terminal when calling program and sets IP and PORT
# to global variables that can be used anywhere
IPADDR = sys.argv[1]
IPPORT = int(sys.argv[2])

# Sets max recieve buffer size in terms of data recieved.
# Used so we can only pull max amount of data from sockets.
RECIEVE_SIZE = 4096


# Class object for Socket Server.
class ThreadSocketServer(object):
    # Sets up server socket information
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Sets up list to contain all connected clients.
    clientConnections = []

    # Initializes the threaded server to bind to ipaddress/port given
    # Starts listening on the connections.
    def __init__(self):
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((IPADDR, IPPORT))
        self.serverSocket.listen(5)
        print("socket now listening for connections.")

    # method to listen for any new connections and starts thread to listen to clients directly.
    def listenForConnection(self):
        while True:

            # Accepts new connection with ip address and saves that data to client, address variables.
            client, address = self.serverSocket.accept()

            # Set timeout to listen to clients (in seconds)
            # When 120 seconds without send/recieve, connection terminates.
            # Change to what suits you best.
            client.settimeout(120)

            # Add new connection to list of connected clients.
            self.clientConnections.append(client)

            # We set listentoclientthread to a thread and start it seperately
            # So we can terminate it later if we really need to by name.
            listentoclientthread = threading.Thread(target=self.listenToClient, args=(client, ), daemon=True)

            # Start thread to listen to client
            listentoclientthread.start()

            # Print new connection to server window to show connection established.
            print("Connection Established " + str(address) + "\nServer >", flush=True)

    # Listens to specific client and runs commands/prints what client sent.
    # this is where you can change what the server does based on what is requested by the client.
    # *REMOTE COMMAND INJECTION SECURITY RISK HERE*
    def listenToClient(self, cl):
        # Continuously listen to client for message. Should be on a thread when creating connection.
        while True:
            # Get message sent by client.
            messageToRecieve = cl.recv(RECIEVE_SIZE)
            # If client dc'ed it sends consistently blank bytes so we check to see if it disconnected.
            if messageToRecieve == b'':
                # If client disconnected, we remove it from our client connections list.
                cl.close()
                self.clientConnections.remove(cl)
                print("Client closed", flush=True)
                sys.exit()
            else:
                # decode the string sent by the client into 'human-readable' format
                messageString = messageToRecieve.decode('utf-8')

                # Check if string received contains the 'command' string in the first word.
                # This will probably change sometime soon. Leaving now to show possible security problem here.
                # i.e 'command ls -la /' will send the client the root directory of the server machine.
                if messageString.split(' ', 1)[0] == "command":

                    # If command present, run command on server and send results to client.
                    # REMOTE COMMAND INJECTION SECUIRTY RISK.
                    # Client can send ANY command they want to the server and get the result.
                    # Be careful with the commands sent. Could cause damage to server machine.
                    commandToRun = messageString.split(' ', 1)[1]
                    commandResponse = subprocess.getoutput(commandToRun)

                    # Print to server what command was run.
                    print("\nCommand Run by client: " + commandToRun + "\nServer >", flush=True)

                    # Send command response to specific client.
                    self.sendToClient(cl, commandResponse)

                else:

                    # Anything else, just show message sent to server.
                    print("Client said: " + messageString + "\nServer >", flush=True)

    # Sends string of data to all clients connected on sockets
    def sendToClients(self, string):
        for cl in self.clientConnections:
            cl.send(string.encode('utf-8'))

    # Sends string of data to specific client in argument.
    def sendToClient(self, cl, string):
        cl.send(string.encode('utf-8'))


# Main Program. Run server.py IP PORT
if __name__ == "__main__":

    # Creates server object that starts listening
    server = ThreadSocketServer()

    # Creates new thread to listen for new connections and creates client listeners in there.
    listenThread = threading.Thread(target=server.listenForConnection, args=(), daemon=True).start()

    # Listens for user input on server to broadcast message to all clients.
    while True:
        # Grabs message/string from user input to broadcast
        messageToSend = input(f"Server >")

        # Checks if message is 'exitserver' to terminate server and close all connections.
        # If yes, close all connections and close server socket.
        if messageToSend == "exitserver":
            sys.exit()
        else:
            # Otherwise just broadcast message to all clients stored in clients list.
            server.sendToClients(messageToSend)
