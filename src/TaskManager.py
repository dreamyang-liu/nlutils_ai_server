import time

from multiprocessing import Process, Queue

from AIServerController import GLOBAL_CONTROLLER
from nlutils.Utils.Log import default_logger
class TaskManager(object):


    def __init__(self):
        self.server_infos = None
        self.ms_queue = Queue()
    
    def run(self):
        default_logger.info(f"TaskManager Running...")
        self._task_dispatcher = Process(target=TaskManager.task_dispatcher, args=(self.ms_queue,))
        self._task_dispatcher.start()
    
    @staticmethod
    def task_dispatcher(msg_queue):
        while True:
            # Server info should be localized for at least one hour to indicate the estimated memory usage of each server. It should be updated per hour and when choseing the device, use the minimum one between realtime server info and localized server info
            server_infos = GLOBAL_CONTROLLER.gpu_manager.get_all_servers()
            task_emitted = False
            for server, server_info in server_infos.items():
                print(server, server_info)
            if not task_emitted:
                # NO TASK EMITTED, NO AVAILABLE DEVICE. WAIT 1 H TO CHECK AGAIN
                time.sleep(3600)
    
    def add_task(self, task):
        self.ms_queue.put(task)
    

if __name__ == "__main__":
    x = TaskManager()
    task_info = {
        "repo_name": "fix",
        "repo_url": "https://github.com/leonard-thong/SciAnnotate.git",
        "timestamp": time.time(),
        "args": "",
        "estimate_cpu_memory": 8000,
        "estimate_gpu_memory": 8000,
        "assigned_gpu_id": 1,
        "assigned_server": "local",
        "launch_script": "train.sh",
        "email": "mliu444@gatech.edu"
    }

    for i in range(50):
        time.sleep(5)
        x.add_task(f'xxx{i}', i * 1200)
        

    