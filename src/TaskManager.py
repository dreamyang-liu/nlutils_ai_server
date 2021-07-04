import time

from multiprocessing import Process, Queue

from utils import gpu_memory_watcher

def emit_task(task, server, device):
    print(task, server, device)


class TaskManager(object):


    def __init__(self):
        self.server_infos = None
        self.task_infos = dict()
        self.ms_queue = Queue()
    
    def run(self):
        self._task_dispatcher = Process(target=TaskManager.task_dispatcher, args=(self.ms_queue,))
        self._task_dispatcher.start()
    
    def load_task_config(self):
        print('Loading task')
        with open('./task.conf', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                task_name = line.split(' ')[0]
                task_minium_memory = int(line.split(' ')[1])
                self.ms_queue.put((task_name, task_minium_memory))
    
    @staticmethod
    def task_dispatcher(msg_queue):
        # TODO Optimzie, find a suitable GPU with minimum available memory
        server_info_cache = {'last_update_timestamp': None, 'server_info': None, 'init': False}
        while True:
            # Server info should be localized for at least one hour to indicate the estimated memory usage of each server. It should be updated per hour and when choseing the device, use the minimum one between realtime server info and localized server info
            server_infos = gpu_memory_watcher()
            if server_info_cache['server_info'] is None:
                server_info_cache['server_info'] = server_infos
            else:
                for server, server_info in server_info_cache['server_info'].items():
                    for idx, device in enumerate(server_info):
                        if time.time() - device['device_info_last_update_timestamp'] >= 3600:
                            server_info_cache['server_info'][server][idx] = server_info[server][idx]
                        
            if server_info_cache['server_info']:
                current_queue_length = msg_queue.qsize()
                task_emitted = False
                for _ in range(current_queue_length):
                    task, task_minium_memory = msg_queue.get()
                    task_assigned = False
                    for server, server_info in server_info_cache['server_info'].items():
                        for device in server_info:
                            if device['device_available_memory'] > task_minium_memory:
                                emit_task(task, server, device)
                                task_emitted = True
                                device['device_available_memory'] -= task_minium_memory
                                device['device_info_last_update_timestamp'] = time.time()
                                task_assigned = True
                            if task_assigned:
                                break
                        if task_assigned:
                            break
                    if not task_assigned:
                        msg_queue.put((task, task_minium_memory))
                if not task_emitted:
                    # NO TASK EMITTED, NO AVAILABLE DEVICE. WAIT 1 H TO CHECK AGAIN
                    time.sleep(3600)
    
    def add_task(self, task, task_minium_memory):
        self.ms_queue.put((task, task_minium_memory))
    

if __name__ == "__main__":
    x = TaskManager()
    x.load_task_config()
    x.run()

    for i in range(50):
        time.sleep(5)
        x.add_task(f'xxx{i}', i * 1200)
        

    