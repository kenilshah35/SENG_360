#!/usr/bin/python3

"""
Last edited by   : Ella
Last edited time : 12/4/2021
"""
import rsa

def rsa_signing_verification(client_username_and_signature,client_public_rsa_key):
    """
    @input : a string that contains the client_username and signature, and client_public_rsa_key
    @output: a boolean value indicates if the signature is correct, and encrypted_client_username 
    """
    client_username_and_signature= client_username_and_signature.split("--SIGNATURE--")
    client_username=client_username_and_signature[0]
    signature=client_username_and_signature[1]
    try:
        # if the system does not raise ValueError, that means the signature is correct.
        rsa.verify(client_username.encode(), signature.encode("latin-1"), client_public_rsa_key)
        return True,client_username
    except ValueError as err:
        print(err)
        return False,client_username

def rsa_signing(message,privkey_rsa):
    """
    @input : message,privkey_rsa
    @output: message--SIGNATURE--privkey_rsa
    """
    signature = rsa.sign(message.encode(), privkey_rsa, 'SHA-1')
    return message+ '--SIGNATURE--'+str(signature.decode("latin-1"))