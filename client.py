# import tools
import socket 
import threading

# Defining constants
SERVERNAME = "127.0.0.1"
PORT = 15000

# Function to listen for messages from server
def listen_for_msgs(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message !='':
            print(f"{message}")
        else:
            print('message received from server is empty')

# Function to send message to server
def send_msg(client):
    while True:
        message = input("Message:")
        if message != '':
            client.sendall(message.encode())
        else:
            print("You cant send an empty message.")

# Function to communicate with server
def communication(client):
    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("username required")
        exit(0)
    # use threads to make sure listen_for_msgs runs all the time without altering the functionality
    # of the client
    threading.Thread(target=listen_for_msgs, args=(client, )).start()

    send_msg(client)

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
    
    communication(clientSocket)

if __name__ == '__main__':
    main()