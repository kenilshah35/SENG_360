#!/usr/bin/python3
"""Client for chat application"""

"""
Last edited by   : Ella
Last edited time : 12/4/2021
"""
from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from rsa_signing import rsa_signing
from key_exchange import key_builder
from time import sleep, ctime
from threading import Thread
import rsa
import getpass
import random
import os
import json
from cryptography.fernet import Fernet

server_partial_key=None
connection_flag=1 # connection_flag would be set off once the Partial_key is obtained.
pass_signal=0
session_chat_history = {} #stores all chat history for the current session
session_id = int(random.uniform(1000,9999)) # Not meaningful
username = None # username of the client
BUFFER_SIZE = 1024
SERVER = gethostbyname(gethostname())
ADDRESS = (SERVER, 5050)
chat_enc_key = None


def connection_handler():
    """ Handles initial connection with the client. """
    global connection_flag
    global pass_signal
    global server_partial_key
    global username
    private_key=int(random.uniform(100,500))
    public_key=int(random.uniform(100,500))
    (pubkey_rsa, privkey_rsa) = rsa.newkeys(1024)

    # send the client public key to the server
    chat_client.send(bytes((str(public_key)+' '), "utf8"))
    connection_flag=1
    sleep(0.2)
    # send partial key to server
    client_key_handler=key_builder(public_key,151,private_key)
    client_partial_key=str(client_key_handler.generate_partial_key())+' '
    chat_client.send(bytes(client_partial_key, "utf8"))
    # obtain full client key
    full_key_client=client_key_handler.generate_full_key(int(server_partial_key))
    sleep(0.1)
    # sending the RSA public key for further identification
    send_message=pubkey_rsa.save_pkcs1("PEM")
    chat_client.send(bytes(send_message))

    sleep(0.1)
    msg = input()
    chat_client.send(bytes(msg, "utf8"))
    sleep(0.2)
    while(pass_signal==0):
        # send the encrypted credentials to server.
        try:
            sleep(0.2)
            username = input("username:  ")
            msg = client_key_handler.encrypt_message(username)
            chat_client.send(bytes(rsa_signing(msg,privkey_rsa), "utf8"))
            sleep(0.1)
            # password = input("password:  ")
            password= getpass.getpass()
            msg = client_key_handler.encrypt_message(password)
            chat_client.send(bytes(rsa_signing(msg,privkey_rsa), "utf8"))
        except ValueError as err:
            os._exit(-1)
        sleep(0.1)

def message_receiver():
    """Receives messages."""
    global connection_flag
    global pass_signal
    global server_partial_key
    while True:
        try:
            msg = chat_client.recv(BUFFER_SIZE).decode("utf8")
            if msg:
                if str.isnumeric(msg) and connection_flag:
                    server_partial_key=msg
                    connection_flag=0
                elif msg == "Account Locked":
                    print("Too many failed attempts, your account has been locked.")
                    os._exit(-1)
                elif msg == "PASS":
                    pass_signal=1
                else:
                    print(msg)
                    if msg in ["Account deleted", "Account already exists.", "Invalid reply."]:
                        os._exit(-1)
            else:
                print("Server connection stopped unexpectedly.")
                os._exit(-1)
        except OSError:  # If the client has left the chat.
            if len(session_chat_history) != 0:
                save_chat_history()
            break

def message_sender(event=None):
    """Sends messages until the user enters {quit}."""
    encryption_flag=1
    while True:
        if encryption_flag:
            connection_handler()
            encryption_flag=0
            # Initialize logging current session's chat history
            session_chat_history[session_id] = []
            #Check if enc key already exists for user. If not create one and save to file
            global chat_enc_key
            key_file_name = 'chat_enc_key_' + username + '.key'
            if os.path.isfile(key_file_name):
                with open(key_file_name, 'rb') as filekey:
                    chat_enc_key = filekey.read()
            else:
                chat_enc_key = Fernet.generate_key()
                with open(key_file_name, 'wb') as filekey:
                    filekey.write(chat_enc_key)
        else:
            msg = input()
            chat_client.send(bytes(msg, "utf8"))
            update_session_chat(msg)
            if msg == "{quit}":
                chat_client.close()
                #saving session chat history as soon as the session is finished
                save_chat_history()
                break

def save_chat_history():
    """ Save chat history. """
    filename = 'chat_log_' + username + '.json'
    try:
        with open(filename, "r+") as json_file:
            data = json.load(json_file)
            data.update(session_chat_history)
            json_file.seek(0)
            json.dump(data, json_file)
    except FileNotFoundError:
        with open(filename, 'w') as json_file:
            json.dump(session_chat_history, json_file)
        os.chmod(filename, 0o700)

def update_session_chat(message):
    """ Update session chat. """
    global session_chat_history
    global session_id
    enc_message = encrypt_chat_log_message(message)
    temp = {
        "timestamp" : ctime(),
        "text" : enc_message.decode()
    }
    session_chat_history[session_id].append(temp)

def encrypt_chat_log_message(message):
    global chat_enc_key

    fernet = Fernet(chat_enc_key)
    enc_message = fernet.encrypt(message.encode())

    return enc_message

#function not used in this implementation
def decrypt_chat_log_message(enc_message):
    global chat_enc_key
    if chat_enc_key == None:
        return enc_message

    fernet = Fernet(chat_enc_key)
    dec_message = fernet.decrypt(enc_message).decode()
    return dec_message

if __name__ == "__main__":

    chat_client = socket(AF_INET, SOCK_STREAM)
    chat_client.connect(ADDRESS)
    receive_thread = Thread(target=message_receiver)
    receive_thread.daemon = True
    receive_thread.start()
    message_sender()
