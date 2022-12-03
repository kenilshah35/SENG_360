#!/usr/bin/python3
"""Server for async chat application"""

"""
Last edited by   : Ella
Last edited time : 12/4/2021
"""

from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from rsa_signing import rsa_signing_verification
from key_exchange import key_builder
from login_handler import add_account, check_account, delete_account, lock_account, login_verification
from threading import Thread, get_ident
from sys import exit
import rsa

clients = {}
addresses = {}
online_users = {}
PUBLIC_KEY=151
PRIVATE_KEY=201
BUFFER_SIZE = 1024
SERVER = gethostbyname(gethostname())
ADDRESS = (SERVER, 5050)

def authentication_handler(client,server_key_handler,client_public_rsa_key):
    """
    @input : client that the server is currently interact with, key_handler that used to decrypt the message
    @output: decrypted_client_username, decrypted_client_password
    """
    client_username_and_signature = client.recv(BUFFER_SIZE).decode("utf8")
    correct_signature,encrypted_client_username=rsa_signing_verification(client_username_and_signature,client_public_rsa_key)
    if correct_signature is False:
        client.close()
    client_username=server_key_handler.decrypt_message(encrypted_client_username)
    client.send(bytes('What is your password?' , "utf8"))
    client_password = client.recv(BUFFER_SIZE).decode("utf8")
    correct_signature,encrypted_client_password=rsa_signing_verification(client_password,client_public_rsa_key)
    if correct_signature is False:
        client.close()
    client_password=server_key_handler.decrypt_message(encrypted_client_password)
    return client_username,client_password
    

def login_handler(client,client_address):
    """ Establish secure key and verify login info """
    # Begin key exchange
    client_public_key = client.recv(BUFFER_SIZE).decode("utf8")
    # send server partial key
    server_key_handler=key_builder(int(client_public_key),PUBLIC_KEY,PRIVATE_KEY)
    server_partial_key=str(server_key_handler.generate_partial_key())
    client.send(bytes(server_partial_key, 'utf8'))
    # receive client partial key
    client_partial_key = client.recv(BUFFER_SIZE).decode("utf8")
    server_full_key = server_key_handler.generate_full_key(int(client_partial_key))
    # the server should now receive the public_rsa_key from client for signature verification.
    client_public_rsa_key=client.recv(BUFFER_SIZE).decode("utf8")
    client_public_rsa_key=rsa.key.PublicKey.load_pkcs1(client_public_rsa_key)

    client.send(bytes('Welcome! Type {login} to begin login or type {signup} to create an account.', "utf8"))
    msg = client.recv(BUFFER_SIZE).decode("utf8")
    if msg == "{login}":
        client.send(bytes('What is your username?', "utf8"))
        client_username, client_password = authentication_handler(client,server_key_handler,client_public_rsa_key)
        failure_tracker=2 # At most 3 login attempts
        is_login_valid = login_verification(client_username,client_password)
        while(is_login_valid != "VALID"):
            if is_login_valid == "LOCKED":
                client.send(bytes("Account Locked", "utf8"))
                return None
            elif failure_tracker == 0:
                client.send(bytes("Account Locked", "utf8"))
                lock_account(client_username)
                return None
            else:
                client.send(bytes("Invalid username or password, please try again", "utf8"))
                client_username,client_password=authentication_handler(client,server_key_handler,client_public_rsa_key)
                failure_tracker-=1
                is_login_valid = login_verification(client_username,client_password)
    elif msg == "{signup}":
        while True:
            client.send(bytes('What is your username?', "utf8"))
            client_username, client_password = authentication_handler(client,server_key_handler,client_public_rsa_key)
            # check if the account already exists
            if check_account(client_username):
                client.send(bytes("Account already exists.", "utf8"))
                return None
            client.send(bytes('Please re-enter account information.' , "utf8"))
            client_username2, client_password2 = authentication_handler(client,server_key_handler,client_public_rsa_key)
            if client_password == client_password2 and client_username == client_username2:
                break
            else:
                client.send(bytes('Passwords or usernames not matching, please try again', "utf8"))
        add_account(client_username, client_password)
    else:
        client.send(bytes("Invalid reply.", "utf8"))
        return None
    client.send(bytes("PASS", "utf8"))
    addresses[client] = client_address
    Thread(target=handle_client, args=(client,client_username)).start()
    

def connections_handler():
    """Accept connections from clients."""
    while True:
        client = None
        client, client_address = chat_server.accept()
        Thread(target=login_handler, args=(client,client_address)).start()
        
            

def handle_client(client,username):  # Takes client socket as argument.
    """Handle a client connection."""
    name = username
    online_users[name] = get_ident()

    welcome = 'Welcome to the chat %s! If you want to leave the chat, type {quit} to exit. Type {online} to list online users.' \
        'type {delete} to delete your account.' % name 
    client.send(bytes(welcome, "utf8"))
    client.send(bytes(list_online_users(), "utf8"))

    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))

    clients[client] = name
    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg == bytes("{quit}", "utf8"):
            # close the connection with the client
            client.send(bytes("{quit}", "utf8"))
            close_connection(client, name)
            break
        elif msg == bytes("{online}", "utf8"):
            # list online users
            client.send(bytes(list_online_users(), "utf8"))
        elif msg == bytes("{delete}", "utf8"):
            # delete account and close client connection
            delete_account(name)
            client.send(bytes("Account deleted", "utf8"))
            close_connection(client, name)
            break
        else:
            broadcast(msg, name+": ")

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def list_online_users():
    """Returns a list of online users in a string form"""
    if len(online_users) == 0:
        str = "No online users\n"
        return str

    str = "\nList of all users online :-\n"
    count = 1
    for name, id in online_users.items():
        str = str + "{}) {} : {}\n".format(count, name, id)
        count = count + 1
    return str

def close_connection(client, name):
    """ Close connection with client and alert chat. """
    client.close()
    del clients[client]
    del online_users[name]
    broadcast(bytes("%s has left the chat." % name, "utf8"))
    broadcast(bytes(list_online_users(), "utf8"))

if __name__ == "__main__":
    chat_server = socket(AF_INET, SOCK_STREAM)
    chat_server.bind(ADDRESS)
    chat_server.listen(5)
    print("Waiting for connections...")
    accept_thread = Thread(target=connections_handler)
    accept_thread.start()
    accept_thread.join()
    chat_server.close()
    exit(0)
