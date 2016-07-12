from socket import *
import sys
import threading

BUF_SIZE = 1600


def recv(client, recv_sem):
    first_time = True
    while True:
        recv_data = client.recv(BUF_SIZE)
        if first_time:
            recv_sem.release()
            first_time = False
        if not recv_data:
            break
        print recv_data.strip()


def main():
    host = 'localhost'
    port = 1234
    addr = (host, port)
    try:
        client = socket(AF_INET, SOCK_STREAM)
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

    except error, arg:
        (errno, err_msg) = arg
        print "Failed: %s, errno = %d" % (err_msg, errno)
        sys.exit()


if __name__ == "__main__":
    main()
