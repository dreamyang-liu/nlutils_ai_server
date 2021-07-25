from AIServerController import GLOBAL_CONTROLLER
from Configure import AISConfigure
import socket
import time
import json
from nlutils.Utils.Log import default_logger
from nlutils.Defines import *

class AIServerSocketStore(object):

    def __init__(self):

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.alias = AISConfigure.get_instance().get_config_info('AiServerAlias').as_string()
        self.host = AISConfigure.get_instance().get_config_info('AiServerHost').as_string()
        self.port = AISConfigure.get_instance().get_config_info('AiServerPort').as_int()
    
    def bind(self):
        host = self.host
        port = self.port
        self.socket.bind((host,port))
        default_logger.info(f"Init AI server {host}:{port} success!")
    
    def handle(self, data):
        received_data = data
        print(received_data)
        received_obj = json.loads(received_data)
        response = GLOBAL_CONTROLLER.command_handler_store[received_obj.get("command_id")].handle(received_obj)
        return response

    def handle_socket(self, sock, address):
        data = sock.recv(1024).decode()
        self.handle(data)
    
    def init_all_workers(self):
        default_logger.info('Initializing all workers...')
        workers = AISConfigure.get_instance().get_config_info('AIWorkerTable').raw()
        for worker in workers:
            worker_host = worker.get('host')
            worker_port = int(worker.get('port'))
            msg = dict()
            msg['server_host'] = self.host
            msg['server_port'] = self.port
            msg['operation_id'] = OPERATION_ID.OPERATION_ID_INIT_WORKER
            GLOBAL_CONTROLLER.sender_proxy.send(worker_host, worker_port, msg)
    
    def run(self):
        default_logger.warn(f"Recving data from AI Worker")
        self.socket.listen(100)
        self.init_all_workers()
        while True:
            try:
                sock, address = self.socket.accept()
                self.handle_socket(sock, address)
            except BlockingIOError:
                pass
    
    def close(self):
        self.socket.close()
    

