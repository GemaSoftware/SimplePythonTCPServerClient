# SimplePythonTCPServerClient
Very basic Python 3 TCP server/client app with multithreading and sockets. Will be updated over time. Server.py can be exploited as of now. Goal is to get computations sent from clients to server and return data back to clients.

###### Server.py is easily exploitable as of now. Can pretty much do remote command execution on wherever the server is running.

## Server Usage:
`python3 server.py <hostname> <port>`
On localhost port 1234:
`python3 server.py localhost 1234`

## Client Usage:
This allows you to connect to the server above:
`python3 client.py <hostname> <port>

As a server and client(s), you can send messages between each other. Clients cannot see other client messages. Server reads all connections.

###### For the clients, as of right now, the server is exploitable by sending the following from a client
`command <any windows/linux/mac command>`
As an example of how this is problematic:
`command ls -la /` will return the root directory with any details you want as the server as the current user.
Getting a reverse shell with this would be a piece of cake, am I right?
This 'command' prefix on the client message will print the output of the command being run on the server host and send it back to the client. This will change soon.
