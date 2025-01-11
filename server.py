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


        # Server will listen for client messages with max length of 2048
        # Listening for command login or registration
        command = connectionSocket.recv(1024).decode('utf-8')
        # check command is not empty
        if command != '':
            # split command into its pieces
            control, username, password = command.split(' ')
            # if user wants to register
            if control == REG_MSG:
                # check if username is not being duplicated
                duplicated_username_flag = 0
                users = db.read_usernames()
                duplicated_username_flag = 0
                for user in users:
                    if username == user[0]:
                        duplicated_username_flag = 1
                        print(f"[DUPLICATION] Username '{username}' is duplicated")
                        send_msg([('~user~', connectionSocket)], "Duplicated username. try again")
                        # !!!!send the message to the client
                        break
                if duplicated_username_flag == 1:
                    send_msg([('~user~', connectionSocket)], "closing the connection")
                    connectionSocket.close()
                    continue
                # add new user to database
                hashed_pswd = hashlib.md5(password.encode()).hexdigest()
                with lock:
                    db.insert_into_users((username, hashed_pswd))
                    print(f"[REGISTRATION] User {username} added to database")
                    send_msg([(username, connectionSocket)], "you are registered")
                    # !!!!send user a message that they are registered and noe they  can login
            elif control == LOGIN_MSG:
                # check if user exist
                stored_pswd = db.check_user(username)
                if stored_pswd:
                    pswd_hashed = hashlib.md5(password.encode()).hexdigest()
                    if pswd_hashed == stored_pswd[0]:
                        print("[PASS!]")
                        online_users.append(('username', connectionSocket))
                        send_msg([], f"{username} joined the chat room.")
                        send_msg([(username, connectionSocket)], f"Hi {username}, welcome to the chat room.")
            else:
                print("[INCORRECT COMMAND]")
                send_msg([('~user~', connectionSocket)], "incorrect command")
                connectionSocket.close()
                continue
        else:
            print("[EMPTY MSG] Command is empty")
            connectionSocket.close()

        # Creat a thread for each connection to handle clients simultaneously 
        # and not to have conflict with server listening for connections
        threading.Thread(target=client_handler, args=(connectionSocket, username,)).start()


if __name__ == "__main__":
    main()