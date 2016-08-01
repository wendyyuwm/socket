__author__ = 'Wendy'
# coding = utf-8

import requests
import json
import socket
import threading

count = 0
lock = threading.Lock()


def weather_report(city_name, semaphore):
    while True:
        semaphore.acquire()
        global count, lock
        # lock.acquire()
        # count += 1
        # lock.release()
        with lock:
            count += 1
        url = "http://apis.baidu.com/heweather/weather/free?city=%s" % city_name
        header_info = {"apikey": "1de13fd399be6afae1b738e6887589c8"}
        try:
            response = requests.get(url, headers=header_info)
            content = json.loads(response.text)["HeWeather data service 3.0"][0]["hourly_forecast"][0]["tmp"]
            print "city: %s, temp: %s" % (city_name, json.dumps(content, indent=2))
        except Exception as e:
            print "\nError: %s, city is %s\n" % (e, city_name)
        # print "city: %s" % city_name


def main():
    sem = threading.Semaphore(value=0)
    citys = ["beijing", "shanghai", "nanjing", "hangzhou", "wuhan", "hefei", "yichang", "guangzhou", "changyang",
            "fujian", "xiamen"]
    for city in citys:
        thread = threading.Thread(target=weather_report, args=(city, sem))
        thread.start()
    host = "localhost"
    port = 1234
    address = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(address)
    except socket.error as Err:
        (errno, error_msg) = Err
        print("Error: %s, errno = %d") % (error_msg, errno)
    s.listen(5)

    while True:
        client_connection, client_address = s.accept()
        print "\n%s connect successful" % str(client_address)
        recv_data = client_connection.recv(1024).strip()
        if not recv_data:
            break
        try:
            if recv_data.lower() == "how many?":
                print recv_data
                times = str(count)
                client_connection.send(times)
                print times + " times"
                continue
            num = int(recv_data)
        except ValueError:
            print "Value Error: %s" % recv_data
            client_connection.close()
            continue
        for i in range(num):
            sem.release()


if __name__ == "__main__":
    main()


