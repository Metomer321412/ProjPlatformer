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

def generate_keys(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537

    d = sympy.mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(plaintext, public_key):
    e, n = public_key
    plaintext_integers = [ord(char) for char in plaintext]
    ciphertext = [pow(char, e, n) for char in plaintext_integers]
    return ciphertext

def decrypt(ciphertext, private_key):
    d, n = private_key
    decrypted_integers = [pow(char, d, n) for char in ciphertext]
    plaintext = ''.join(chr(char) for char in decrypted_integers)
    return plaintext

def main():
    p = 2957
    q = 3571
    public_key, private_key = generate_keys(p, q)

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
    counter2 = 0
    print(counter)
    print("idk")

    while (counter !=2 ):
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
                print(recsign)
                if recsign[:4]=="sign":
                    print("input from client sign " + recsign)
                    splt1 = recsign.split("sign")
                    words1 = splt1[1].split(",")
                    username1 = words1[0]
                    password1 = words1[1]
                    print(username1 + " AND " + password1)
                    RSAusr  = encrypt(username1, public_key)
                    print(f"Encrypted ciphertext: {RSAusr}")
                    RSApass = encrypt(password1, public_key)
                    print(f"Encrypted ciphertext: {RSApass}")
                    DATABASE.add_user(str(RSAusr),str(RSApass))
                    print("usernamesign= " + str(RSAusr))
                    print("passwordsign= " + str(RSApass))
                    DATABASE.printall()

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
                    print("usernamelog= " + str(RSAusr2))
                    print("passwordlog= " + str(RSApass2))
                    if DATABASE.authenticate_user(str(RSAusr2),str(RSApass2)):
                        counter +=1
                        print(counter)
                        print('yes')

                        clnt.send("true".encode())
                    else:
                        print('no')
                        clnt.send("no".encode())

                elif recsign=="start":
                    counter2+=1
                    print("start rec")
                    clnt.send('not yet'.encode())

    print("counter2 " + str(counter2))
    while(counter2 !=2):
        readable, _, _ = select.select(inputs, [], [], 0.00000001)
        for sock in readable:
            strcv = None
            if sock.getpeername() == address1:
                acc = client_socket1
                strt = client_socket1.recv(1024)
                strcv = strt.decode()
            else:
                acc = client_socket2
                strt = client_socket2.recv(1024)
                strcv = strt.decode()
            if strcv == 'start':
                counter2+=1
    print("ready")
    client_socket1.send('yes'.encode())
    client_socket2.send('yes'.encode())


    ALLBUTTONS = ["W", "A", "D", "S", "F", "R", "P", "C"]
    RELEASE = ["2A","2D"]
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



if __name__ == "__main__":
    main()