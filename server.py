# import tools
import socket 
import threading

# Defining constants IP and PORT
IP = '127.0.0.1' # local host
PORT = 15000
CONNECTION_LIMIT = 10
online_users = []

# Function to send message to one client
def send_msg_to_client(client, message):
    client.sendall(message.encode())


# Function to send message to chat
def send_msg(receivers: list, message):
    if len(receivers) == 0:
        receivers = online_users
    for receiver in receivers:
        send_msg_to_client(receiver[1], message )


# Function to listen for upcoming messages
def listen_for_msgs(client, username):
    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            print(f"MESSAGE FROM {username}: {msg}")
            final_msg = f"""<{username}>{msg}"""
            send_msg([], final_msg)

        else:
            print(f"Empty message from client {username}")


# Client handler function
def client_handler(client):
    # Server will listen for client messages with max length of 2048
    while True:
        # Listening for username
        username = client.recv(1024).decode('utf-8')
        if username != '':
            duplicated_username_flag = 0
            for user in online_users:
                if username in user:
                    duplicated_username_flag = 1
            if duplicated_username_flag:
                print(f"username '{username}' is duplicated")
            else:
                online_users.append((username, client))
                new_user_msg = f"<CHATBOT> '{username}' joined the chat!"
                send_msg([], new_user_msg)
                break
        else:
            print("username is empty")
    # Because we don't want to have conflict with server listening for connection
    threading.Thread(target=listen_for_msgs, args=(client, username,)).start()

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
        # and not to have conflict with server listening for connections
        threading.Thread(target=client_handler, args=(connectionSocket, )).start()


if __name__ == "__main__":
    main()