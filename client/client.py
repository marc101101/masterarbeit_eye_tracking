#!/usr/bin/python
import sys
import socketio
import time
import ast


class ClientGazeLogger:

    client_name = ""
    sio = None
    connection_attempt = 0

    def __init__(self, ip_address, client_name):
        self.client_name = client_name
        self.sio = socketio.Client()
        try:
            self.connect_to_socket( ip_address)
        except Exception as e:
            print("Server not reachable ... Try to connect")
            self.connect_to_socket(ip_address)

        self.watch_data_stream()

    def connect_to_socket(self, ip_address):
        if(self.connection_attempt <= 5):
            self.connection_attempt += 1
            self.sio.connect('http://' + ip_address + ':5000')
        else:
            print("Not able to connect to server. Try again later.")
            sys.exit()

    def watch_data_stream(self):
        k = 0

        try:
            buff = ''
            while True:
                buff += sys.stdin.read(1)
                if buff.startswith("relevant_entry"):
                    if buff.endswith('\n'):
                        print("Message received!")
                        message_to_push = str(buff)[15:]
                        message_to_push = ast.literal_eval(message_to_push)
                        message_to_push['timestamp'] = time.time()
                        message_to_push['client_id'] = self.client_name
                        print(message_to_push)
                        try:
                            self.push_to_server(message_to_push)
                        except Exception as e:
                            print(e)
                        buff = ''
                        k = k + 1
                else:
                    if buff.endswith('\n'):
                        print(buff[:-1])
                        buff = ''

        except KeyboardInterrupt:
            sys.stdout.flush()
            pass
        print("End of Log: " + str(k))

    def push_to_server(self, message):
        self.sio.emit('message', message)


if __name__ == "__main__":
    print("INFO: Client  up and tracking")
    print("INFO: IP address - " + str(sys.argv[1]))
    print("INFO: Client name - " + str(sys.argv[2]))

    client = ClientGazeLogger(sys.argv[1], sys.argv[2])

