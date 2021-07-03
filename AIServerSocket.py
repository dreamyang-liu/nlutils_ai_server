import socket
import time
from nlutils.Utils.Log import default_logger

class AIServerSocketStore(object):

    def __init__(self, alias):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.socket.setblocking(0)
        self.alias = alias
    
    def bind(self,host,port):
        self.socket.bind((host,port))
        default_logger.info(f"Init AI server {host}:{port} success!")
    
    def handle(self, sock, address):
        data = sock.recv(1024).decode()
        default_logger.info(f"AI Worker {address}: {data}")
    
    def run(self):
        default_logger.warn(f"Recving data from AI Worker")
        self.socket.listen(100)
        while True:
            try:
                sock, address = self.socket.accept()
                self.handle(sock, address)
            except BlockingIOError:
                pass
    
    def close(self):
        self.socket.close()
    

