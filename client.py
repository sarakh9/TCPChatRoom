# import tools
import socket 
import threading

# Defining constants
SERVERNAME = "127.0.0.1"
PORT = 15000

# Main function
def main():
    # Creating Client Socket using IPV4 address family(AF_INET) and TCP protocol(SOCK_STREAM)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Connect to the server
    try:
        clientSocket.connect((SERVERNAME, PORT))
        print("Connected to the server")
    except Exception:
        print(f"{Exception}: cannot connect to the server {SERVERNAME} {PORT}")

if __name__ == '__main__':
    main()