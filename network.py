import socket
import pickle


class WrongIp(Exception):
    pass

class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.server = self.ip
        self.port = 5555
        self.addr = (self.server, self.port)


    def connect(self, name, color):
        try:
            self.client.connect(self.addr)
            self.client.send(pickle.dumps((name, color)))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096*2))
        except socket.error as e:
            print(e)

    # def send_nick(self, data):
    #     try:
    #         self.client.send(str.encode(data))
    #         return pickle.loads(self.client.recv(2048))
    #     except socket.error as e:
    #         print(e)