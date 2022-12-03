#!/usr/bin/python3

"""
Last edited by   : Ella
Last edited time : 12/4/2021
"""
from Crypto.Cipher import AES

class aes_cbc():
    def __init__(self,key,iv):
        self.key = self.padding(key)
        self.model = AES.MODE_CBC
        self.iv = iv.encode()

    def padding(self,message):
        if type(message) == str:
            message = message.encode()
        while len(message) % 16 != 0:
            message += b'\x00'
        return message

    def aesEncrypt(self,text):
        padded_txt = self.padding(text)
        self.aes = AES.new(self.key,self.model,self.iv) 
        self.encrypt_text = self.aes.encrypt(padded_txt)
        return self.encrypt_text

    def aesDecrypt(self,text):
        self.aes = AES.new(self.key,self.model,self.iv) 
        self.decrypt_text = self.aes.decrypt(text)
        self.decrypt_text = self.decrypt_text.strip(b"\x00")
        return self.decrypt_text

