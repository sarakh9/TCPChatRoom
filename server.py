# import tools
import socket 
import threading

# Defining constants IP and PORT
IP = '127.0.0.1' # local host
PORT = 15000
CONNECTION_LIMIT = 10

# Public message function
def public_message(srnder, message):
    pass

# Private message function
def public_message(srnder, message):
    pass

# Client handler function
def client_handler(client):
    pass

# Main function
def main():
    # Creating Server Socket using IPV4 address family(AF_INET) and TCP protocol(SOCK_STREAM)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind server socket to port 15000 and ip 127.0.0.1
    try:
        serverSocket.bind((IP, PORT))
        print("Server is running...")
        print(f"SERVER IP:{IP} PORT: {PORT}")
    except Exception:
        print(f"ERROR : Unable to bind to ip {IP} and port {PORT}")
    
    # Start listening on port 15000
    serverSocket.listen(CONNECTION_LIMIT)
    print("The server is ready to receive")

    # Keep listening for client connection request on loop
    while True:
        # Accept connection request, create a connection socket and save the clients address(ip, port)
        connectionSocket, addr = serverSocket.accept()
        print(f"Succesfully connected to client with ip: {addr[0]} and port: {addr[1]}")

        # Creat a thread for each connection to handle clients simultaneously
        threading.Thread(target=client_handler, args=(connectionSocket, )).start()


if __name__ == "__main__":
    main()