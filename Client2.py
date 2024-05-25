import socket
IP = '127.0.0.1'
PORT = 1729


def main():
    """Main function"""
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('0.0.0.0', 1445))
    my_socket.connect((IP, PORT))
    while (True):
        my_socket.send("hi".encode())
        msg = my_socket.recv(1024)
        print(msg.decode())
if __name__ == "__main__":
    main()