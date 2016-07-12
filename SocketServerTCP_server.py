from socket import *
import threading
import sys

BUF_SIZE = 1600


def send(client_name_sock):
    while True:
        try:
            send_data = raw_input("")
            name = send_data.split(":")[0]
            if name in client_name_sock.keys():
                sock = client_name_sock[name]
                sock.send(send_data.split(":")[1])

        except error as arg:
            (errno, err_msg) = arg
            print "Error: %s, errno = %d" % (err_msg, errno)
            # sys.exit()   modify error type

        finally:
            sock.close()


def recv(client_sock):
    while True:
        try:
            recv_data = client_sock.recv(BUF_SIZE).strip()
            if not recv_data:
                break
            print recv_data

        except error as arg:
            (errno, err_msg) = arg
            print "Error: %s, errno = %d" % (err_msg, errno)
            # sys.exit() modify error type

        finally:
            client_sock.close()

def user_password(client_sock, ):
    temp_dir= {}
    client_sock.send("New Client? (Y)es or (N)o: ")
    new_user = client_sock.recv(1024).strip()
    client_conn.send("Enter the client name: ")
    name = client_sock.recv(1024).strip()
    client_conn.send("Please enter the password: ")
    password = client_sock.recv(1024).strip()
    temp_dir[name] = client_sock
    if new_user.upper() == "Y":
        client_dir[name] = password


def main():
    host = "localhost"
    port = 1234
    server_addr = (host, port)
    try:
        client_dir = {}
        temp_dir = {}
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(server_addr)
        s.listen(50)
        while True:
            (client_conn, client_addr) = s.accept()
            client_conn.send("New Client? (Y)es or (N)o: ")
            new_user = client_conn.recv(1024).strip()
            client_conn.send("Enter the client name: ")
            name = client_conn.recv(1024).strip()
            client_conn.send("Please enter the password: ")
            password = client_conn.recv(1024).strip()
            temp_dir[name] = client_conn
            if new_user.upper() == "Y":
                client_dir[name] = password
                send_thread = threading.Thread(target=send, args=(temp_dir, ))
                send_thread.start()
                recv_thread = threading.Thread(target=recv, args=(client_conn,))
                recv_thread.start()
            elif new_user.upper() == "N":
                # print client_dir
                if client_dir[name] == password:
                    send_thread = threading.Thread(target=send, args=(temp_dir, ))
                    send_thread.start()
                    recv_thread = threading.Thread(target=recv, args=(client_conn,))
                    recv_thread.start()
                else:
                    print "Wrong PassWord!!\t\t...Quit...\n"
                    sys.exit()
            else:
                print "Enter the wrong command\t\t...Quit...\n"
                sys.exit()
            print client_dir
            del temp_dir

    except error, arg:
        (errno, err_msg) = arg
        print "Error: %s, errno = %d" % (err_msg, errno)
        sys.exit()

    s.close()

if __name__ == "__main__":
    print "Server is running..."
    main()

