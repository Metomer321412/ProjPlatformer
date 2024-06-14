import socket
import select
import database
import os
import tkinter as tk
from tkinter import *
import sympy
import random
from database import DATABASE
from pathlib import Path
import sqlite3
IP = '0.0.0.0'
PORT = 1729
PATH = Path(__file__).parent / "data.db"

def generate_keys(bit_length=1024):
    # Generate two large prime numbers p and q
    p = sympy.randprime(2**(bit_length//2 - 1), 2**(bit_length//2))
    q = sympy.randprime(2**(bit_length//2 - 1), 2**(bit_length//2))

    # Compute n (modulus) and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose an integer e such that 1 < e < phi_n and gcd(e, phi_n) = 1
    e = 65537  # It's common to use 65537 as the public exponent

    # Compute the private key d, the modular multiplicative inverse of e modulo phi_n
    d = sympy.mod_inverse(e, phi_n)

    # Public key (e, n) and private key (d, n)
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(plaintext, public_key):
    e, n = public_key
    # Convert each character in the plaintext to its corresponding integer
    plaintext_integers = [ord(char) for char in plaintext]
    # Encrypt each integer using the public key
    ciphertext = [pow(char, e, n) for char in plaintext_integers]
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    # Decrypt each integer in the ciphertext using the private key
    decrypted_integers = [pow(char, d, n) for char in ciphertext]
    # Convert each decrypted integer back to its corresponding character
    plaintext = ''.join(chr(char) for char in decrypted_integers)
    return plaintext

def main():
    class Db:
        def __init__(self, table_name: str) -> None:
            self.__table_name = table_name
            self.__con = sqlite3.connect(PATH)
            self.__cursor = self.__con.cursor()

            self.__setup_table()

        def __setup_table(self) -> None:
            self.__cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.__table_name} (user_name TEXT PRIMARY KEY, password TEXT)
            """)

    public_key, private_key = generate_keys()

    fnal =False
    plcmnt = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(2)
    inputs = []

    client_socket1, address1 = server_socket.accept()
    print(address1)
    client_socket1.send("1".encode())
    inputs.append(client_socket1)

    client_socket2, address2 = server_socket.accept()
    print(address2)
    client_socket2.send("2".encode())
    inputs.append(client_socket2)
    counter = 0
    print(counter)
    print("idk")
    while (counter !=2 ):
    #    print(counter)
        readable, _, _ = select.select(inputs, [], [], 0.00000001)
        for sock in readable:
            print("stuck")
            recsign = None
            if sock.getpeername() == address1:
                clnt=client_socket1
                print("1")
                recmsg = client_socket1.recv(1024)
                recsign = recmsg.decode()
                print("input from client1 " + recsign)
            else:
                clnt=client_socket2
                print("2")
                recmsg = client_socket2.recv(1024)
                recsign = recmsg.decode()
                print("input from client2 " + recsign)
            if recsign !=None:
                if recsign[:4]=="sign":
                    print("input from client sign " + recsign)
                    splt1 = recsign.split("sign")
                    words1 = splt1[1].split(",")
                    username1 = words1[0]
                    password1 = words1[1]
                    print(username1 + "," + password1)
                    RSAusr  = encrypt(username1, public_key)
                    print(f"Encrypted ciphertext: {RSAusr}")
                    RSApass = encrypt(password1, public_key)
                    print(f"Encrypted ciphertext: {RSApass}")
                    DATABASE.add_user(str(RSAusr),str(RSApass))

                elif recsign[:3]=="log":
                    print("input from client log " + recsign)
                    splt2 = recsign.split("log")
                    words2 = splt2[1].split(",")
                    username2 = words2[0]
                    password2 = words2[1]
                    print(username2 + "," + password2)
                    RSAusr2 = encrypt(username2, public_key)
                    print(f"Encrypted ciphertext: {RSAusr2}")
                    RSApass2 = encrypt(password2, public_key)
                    print(f"Encrypted ciphertext: {RSApass2}")
                    if DATABASE.authenticate_user(str(RSAusr2),str(RSApass2)):
                        counter +=1
                        print(counter)
                        print('yes')

                        clnt.send("true".encode())
                    else:
                        print('no')
                        clnt.send("no".encode())


    ALLBUTTONS = ["W", "A", "D", "S", "F", "R", "P", "C"]
    RELEASE = ["2A","2D"]
    #msg = client_socket2.recv(1024)
    while (True):
        readable, _, _ = select.select(inputs, [], [],0.00000001)
        for sock in readable:

            if sock.getpeername() == address1:
                msg1 = client_socket1.recv(1024)
                but = msg1.decode()
                if but in ALLBUTTONS or but in RELEASE:
                    print("input from client1 " + but)
                    client_socket2.send(but.encode())
            else:
                msg2 = client_socket2.recv(1024)
                but = msg2.decode()
                if but in ALLBUTTONS or but in RELEASE:
                    print("input from client2 " + but)
                    client_socket1.send(but.encode())

            #print(msg.decode())
      #  print(msg2.decode())
        #print(address1)
        #print(address2)

if __name__ == "__main__":
    main()