from Configure import AISConfigure
from nlutils.Utils.Log import default_logger
from nlutils.Defines import OPERATION_ID
from AIServerController import GLOBAL_CONTROLLER
from multiprocessing import Process
import time

class GPUServerManager(object):

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GPUServerManager, cls).__new__(cls,*args,**kwargs)
        return cls.instance

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, 'inited'):
            cls.inited = True
            cls.server_dict = dict()
        return cls
    
    @classmethod
    def run(cls):
        cls.fetcher = Process(target=cls.fetch_gpu_summary)
        cls.fetcher.start()
    
    @staticmethod
    def fetch_gpu_summary():
        while True:
            default_logger.info("Fetching GPU Summary...")
            msg = dict()
            msg['server_host'] = AISConfigure.get_instance().get_config_info('AiServerHost').as_string()
            msg['server_port'] = AISConfigure.get_instance().get_config_info('AiServerPort').as_int()
            msg['operation_id'] = OPERATION_ID.OPERATION_ID_UPDATE_GPU_SUMMARY
            workers = AISConfigure.get_instance().get_config_info('AIWorkerTable').raw()
            for worker in workers:
                try:
                    host = worker.get('host')
                    port = int(worker.get('port'))
                    GLOBAL_CONTROLLER.sender_proxy.send(host, port, msg)
                except ConnectionRefusedError:
                    default_logger.error(f"Unable to connect ai worker [{worker.get('alias')}]")
            time.sleep(10)
    
    @classmethod
    def register_server(cls, server):
        server_alias = server.get('worker_alias')
        cls.server_dict[server_alias] = server
    
    @classmethod
    def update_server(cls, server):
        cls.register_server(server)
    
    @classmethod
    def get_server(cls, alias):
        if alias in cls.server_dict.keys():
            return cls.server_dict[alias]
        else:
            default_logger.error(f"Server Alias [{alias}] not registered")
            return None
    
    @classmethod
    def get_all_servers(cls):
        return cls.server_dict
