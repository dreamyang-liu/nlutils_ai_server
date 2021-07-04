from nlutils_ai_server.OperationHandler import OPERATION_DISPATCHER
import socket
import time
import json
from nlutils.Utils.Log import default_logger

class AIServerSocketStore(object):

    def __init__(self, alias):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.alias = alias
    
    def bind(self,host,port):
        self.socket.bind((host,port))
        default_logger.info(f"Init AI server {host}:{port} success!")
    
    def handle(self, data):
        received_data = data.decode("utf-8")
        received_obj = json.loads(received_data)
        response = OPERATION_DISPATCHER[received_obj.get("operation_id")].handle(received_obj)
        return response

    def handle_socket(self, sock, address):
        data = sock.recv(1024).decode()
        self.handle(data)
    
    def run(self):
        default_logger.warn(f"Recving data from AI Worker")
        self.socket.listen(100)
        while True:
            try:
                sock, address = self.socket.accept()
                self.handle_socket(sock, address)
            except BlockingIOError:
                pass
    
    def close(self):
        self.socket.close()
    

