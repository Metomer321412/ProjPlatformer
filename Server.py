import socket
import select
import os
IP = '0.0.0.0'
PORT = 1729
def main():
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