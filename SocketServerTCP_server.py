# coding = utf-8
from socket import *
import threading
import sys

BUF_SIZE = 1600
TEMP_DIR = {}


def send(name_sock_map):
    while True:
        send_data = raw_input("")
        if send_data.find(":") == -1:
            print("Format Error!")
            break
        name = send_data.split(":")[0]
        if name not in name_sock_map.keys():
            print("Client is not OnLine\n")
            break
        sock = name_sock_map[name]
        try:
            sock.send(send_data.split(":")[1])
        except error as arg:
            (errno, err_msg) = arg
            print "Error: %s, errno = %d" % (err_msg, errno)
            if errno == 10054:
                sock.close()
            break


def recv(client_sock):
    while True:
        try:
            recv_data = client_sock.recv(BUF_SIZE)
            if not recv_data:
                break
            print recv_data.strip()
        except error as arg:
            (errno, err_msg) = arg
            print "Error: %s, errno = %d" % (err_msg, errno)
            if errno == 10054:
                client_sock.close()
                break


def user_password(client_sock):
    try:
        client_dir = {}
        client_sock.send("New Client? (Y)es or (N)o: ")
        new_user = client_sock.recv(1024).strip()
        client_sock.send("Enter the client name: ")
        name = client_sock.recv(1024).strip()
        client_sock.send("Please enter the password: ")
        password = client_sock.recv(1024).strip()
        TEMP_DIR[name] = client_sock
        if new_user.upper() == "Y":
            client_dir[name] = password
            return True
        elif new_user.upper() == "N":
            if client_dir[name] == password:
                return True
            else:
                print "Wrong PassWord!!\t\t...Quit...\n"
                return False
        else:
            print "Enter the wrong command\t\t...Quit...\n"
            return False

    except error as arg:
        (errno, err_msg) = arg
        print "Error: %s, errno = %d" % (err_msg, errno)
        if errno == 10054:
            client_sock.close()
        else:
            return False


def main():
    host = "localhost"
    port = 1234
    server_addr = (host, port)
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.bind(server_addr)
    except error as arg:
        (errno, err_msg) = arg
        print "Bind Failed: %s, errno = %d" % (err_msg, errno)
        sys.exit()
    s.listen(5)
    while True:
        (client_conn, client_addr) = s.accept()
        print client_conn
        if user_password(client_conn) is True:
            print TEMP_DIR
            send_thread = threading.Thread(target=send, args=(TEMP_DIR, ))
            send_thread.start()
            recv_thread = threading.Thread(target=recv, args=(client_conn,))
            recv_thread.start()
    s.close()

if __name__ == "__main__":
    print "Server is running..."
    main()

