__author__ = 'Wendy'
# coding = utf-8

import socket
import sys


def main():
    server_host = "localhost"
    server_port = 1234
    server_addr = (server_host, server_port)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect(server_addr)
    except socket.error as error:
        (errno, err_msg) = error
        print("Error:%s, error no is %d") %(errno, err_msg)
    send_data = raw_input("")
    if not send_data:
        sys.exit()
    client_sock.sendall(send_data)
    if send_data.lower() == "how many?":
        try:
            recv_data = client_sock.recv(1024)
            if not recv_data:
                sys.exit()
            print "%s times" % recv_data
        except socket.error as error:
            (errno, err_msg) = error
            print("Error:%s, error no is %d") %(errno, err_msg)
    client_sock.close()

if __name__ == "__main__":
    main()
