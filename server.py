# import tools and modules
import socket 
import threading
import hashlib
from users_model import User

# Defining constants IP and PORT
IP = '127.0.0.1' # local host
PORT = 15000
CONNECTION_LIMIT = 10
DISCONNECT_MSG = "Bye."
REG_MSG = "REGISTERATION"
LOGIN_MSG = "LOGIN"
online_users = []
db = User()

lock = threading.Lock()

# Function to send message to one client
def send_msg_to_client(client, message):
    client.sendall(message.encode())


# Function to send message to chat
def send_msg(receivers: list, message):
    if len(receivers) == 0:
        receivers = online_users
    for receiver in receivers:
        send_msg_to_client(receiver[1], message )



# Client handler function
def client_handler(client, username):
    try:
        connected =True
        while connected:
            msg = client.recv(2048).decode('utf-8')
            if msg != '':
                print(f"MESSAGE FROM {username}: {msg}")
                final_msg = f"""<{username}>{msg}"""
                send_msg([], final_msg)
            else:
                print("[EMPTY MSG] Message is empty")
                # !!!! tell user they can't send empty message
    finally:
        pass
    # Because we don't want to have conflict with server listening for connection
    # threading.Thread(target=listen_for_msgs, args=(client, username,)).start()

# Main function
def main():
    # Creating Server Socket using IPV4 address family(AF_INET) and TCP protocol(SOCK_STREAM)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind server socket to port 15000 and ip 127.0.0.1
    try:
        serverSocket.bind((IP, PORT))
        print("[SERVER RUNNING]")
        print(f"SERVER IP:{IP} PORT: {PORT}")
    except Exception:
        print(f"[ERROR] Unable to bind to ip {IP} and port {PORT}")
    
    # Start listening on port 15000
    serverSocket.listen(CONNECTION_LIMIT)
    print("[LISTENING...]")

    # Keep listening for client connection request on loop
    while True:
        # Accept connection request, create a connection socket and save the clients address(ip, port)
        connectionSocket, addr = serverSocket.accept()
        print(f"[NEW CONNECTION] Succesfully connected to client with ip: {addr[0]} and port: {addr[1]}")

        
               
        first_msg = F"""WELCOME TO SIMPLE TCP CHATROOM!
HERE YOU CAN CREATE AN ACCOUNT, SEND PUBLICK AND PRIVATE MESSAGES.
IF YOU'RE NEW HERE, TO START SEND THIS MESSAGE TO CREATE YOUR ACCOUNT: REGISTERATION <USERNAME> <PASSWORD>
AND TO LOGIN SEND THIS MESSAGE: LOGIN <USERNAME> <PASSWORD>.
NOTE: DO NOT USE SPACE IN YOUR USSERNAME AND IN YOUR PASSWORD!
NOTE2: AFTER YOU REGISTERED YOU WILL NEED TO RESTART!"""
        send_msg([('new_conn', connectionSocket)], first_msg)

        # Server will listen for client messages with max length of 2048
        # Listening for command login or registration
        command = connectionSocket.recv(1024).decode('utf-8')
        # check command is not emppty
        if command != '':
            # split command into its pieces
            control, username, password = command.split(' ')
            # if user wants to register
            if control == REG_MSG:
                # check if username is not being duplicated
                duplicated_username_flag = 0
                users = db.read_usernames()
                for user in users:
                    if username == user:
                        duplicated_username_flag = 1
                    if duplicated_username_flag:
                        print(f"[DUPLICATION] Username '{username}' is duplicated")
                        # !!!!send the message to the client
                        break
                # add new user to database
                if duplicated_username_flag == 0:
                    hashed_pswd = hashlib.md5(password.encode())
                    with lock:
                        db.insert_into_users((username, hashed_pswd))
                        print("[REGISTRATION] User {username} added to database")
                        # !!!!send user a message that they are registered and noe they  can login
            elif command == LOGIN_MSG:
                pass
            else:
                pass
            duplicated_username_flag = 0
            for user in online_users:
                if username in user:
                    duplicated_username_flag = 1
            if duplicated_username_flag:
                print(f"[DUPLICATION] Username '{username}' is duplicated")
            else:
                online_users.append((username, connectionSocket))
                new_user_msg = f"<CHATBOT> '{username}' joined the chat!"
                send_msg([], new_user_msg)
                break
        else:
            print("[EMPTY MSG] Command is empty")

        # Creat a thread for each connection to handle clients simultaneously 
        # and not to have conflict with server listening for connections
        threading.Thread(target=client_handler, args=(connectionSocket, username,)).start()


if __name__ == "__main__":
    main()