#!/usr/bin/python3
import aes_encryption
import random

"""
Last edited by: Ella
Last edited time : 12/4/2021
"""

class DH_key_constructor(object):
    def __init__(self, client_public_key, server_public_key, private_key):
        self.client_public_key = client_public_key
        self.server_public_key = server_public_key
        self.private_key = private_key
        self.full_key = None
        
    def generate_partial_key(self):
        partial_key = self.client_public_key**self.private_key
        partial_key = partial_key%self.server_public_key
        return partial_key
    
    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key%self.server_public_key
        self.full_key = full_key
        return full_key
        
    def encrypt_message(self, message):
        random_iv = ''
        iv=random_iv.join(random.choice("0123456789") for i in range(16))
        aes_cbcor = aes_encryption.aes_cbc(str(self.full_key),iv)
        en_text = aes_cbcor.aesEncrypt(message).decode('latin-1')
        encrypted_message=en_text+"--IV--"+iv
        return encrypted_message
    
    def decrypt_message(self, encrypted_message):
        encrypted_message_and_iv= encrypted_message.split("--IV--")
        encrypted_message=encrypted_message_and_iv[0].encode('latin-1')
        iv=encrypted_message_and_iv[1]
        aes_cbcor = aes_encryption.aes_cbc(str(self.full_key),iv)
        text = aes_cbcor.aesDecrypt(encrypted_message).decode()
        return text

def key_builder(public_key,target_pub_key,private_key) -> DH_key_constructor:
    return DH_key_constructor(public_key,target_pub_key,private_key)
