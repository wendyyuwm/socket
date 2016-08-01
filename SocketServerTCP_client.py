#encoding:utf-8
# from socket import *
import socket
import sys
import threading

BUF_SIZE = 1600


def recv(client, recv_sem):
    first_time = True
    while True:
        try:
            recv_data = client.recv(BUF_SIZE)
            if first_time:
                recv_sem.release()
                first_time = False
            if not recv_data:
                break
            print recv_data.strip()
        except socket.error as arg:
            (errno, err_msg) = arg
            if errno == 9:
                break
            print "Failed: %s, errno = %d" % (err_msg, errno)
            sys.exit()



def main():
    host = 'localhost'
    port = 1234
    addr = (host, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(addr)
        recv_semaphore = threading.Semaphore(value=0)
        recv_thread = threading.Thread(target=recv, args=(client, recv_semaphore))
        recv_thread.start()
        recv_semaphore.acquire(blocking=True)
        while True:
            send_data = raw_input("")
            if not send_data or send_data == "exit":
                break
            client.send('%s' % send_data)
        client.close()

    except socket.error as arg:
        print arg
        (errno, err_msg) = arg
        print "Failed: %s, errno = %d" % (err_msg, errno)
        client.close()
        sys.exit()


if __name__ == "__main__":
    main()
